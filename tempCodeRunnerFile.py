@BP.route('/budget', methods=['GET', 'POST'])
@login_required_manual
def budget():
    user = get_current_user()
    if not user:
        return redirect(url_for('BP.login'))

    if not user.budget:
        # Initialize budget if it doesn't exist (same as before)
        budget = Budget(curr_total_budget=user.income)
        
        accommodation = Accommodation(acc_budget=0.0, acc_current=0.0)
        entertainment = Entertainment(ent_budget=0.0, ent_current=0.0)
        food = Food(food_budget=0.0, food_current=0.0)
        transportation = Transportation(trs_budget=0.0, trs_current=0.0)
        subscription = Subscription(subs_budget=0.0, subs_current=0.0)
        other = Other(other_budget=0.0, other_current=0.0)
        
        db.session.add_all([accommodation, entertainment, food, transportation, subscription, other])
        db.session.commit()
        
        budget.accommodation = accommodation
        budget.entertainment = entertainment
        budget.food = food
        budget.transportation = transportation
        budget.subscription = subscription
        budget.other = other

        db.session.add(budget)
        db.session.commit()
        
        user.budget = budget
        db.session.commit()
    else:
        budget = user.budget

    # Handle POST requests (spending)
    if request.method == 'POST':
        action = request.form.get('action')  # Only 'spend' for budget page
        amount = float(request.form.get('amount', 0))
        category = request.form.get('category')
        detail = request.form.get('detail', '')
        date = datetime.utcnow()

        if not budget:
            flash("Budget not set up.", "error")
            return redirect(url_for('BP.budget'))

        if action == 'spend':
            # Map categories to their respective models and fields
            category_map = {
                'accommodation': ('accommodation', 'acc_current'),
                'entertainment': ('entertainment', 'ent_current'),
                'food': ('food', 'food_current'),
                'transportation': ('transportation', 'trs_current'),
                'subscription': ('subscription', 'subs_current'),
                'other': ('other', 'other_current')
            }

            if category not in category_map:
                flash("Invalid category selected.", "error")
                return redirect(url_for('BP.budget'))

            rel_name, current_attr = category_map[category]
            category_obj = getattr(budget, rel_name)

            # Create category record if it doesn't exist
            if not category_obj:
                if rel_name == 'accommodation':
                    category_obj = Accommodation(acc_budget=0, acc_current=0)
                elif rel_name == 'entertainment':
                    category_obj = Entertainment(ent_budget=0, ent_current=0)
                elif rel_name == 'food':
                    category_obj = Food(food_budget=0, food_current=0)
                elif rel_name == 'transportation':
                    category_obj = Transportation(trs_budget=0, trs_current=0)
                elif rel_name == 'subscription':
                    category_obj = Subscription(subs_budget=0, subs_current=0)
                elif rel_name == 'other':
                    category_obj = Other(other_budget=0, other_current=0)
                
                db.session.add(category_obj)
                db.session.flush()  # Get the ID
                setattr(budget, f"{rel_name}_id", getattr(category_obj, f"{rel_name}_id"))
                setattr(budget, rel_name, category_obj)

            # Check if total budget has enough funds
            if budget.curr_total_budget >= amount:
                # Deduct from total budget
                budget.curr_total_budget -= amount
                
                # Add to category spending (track as positive)
                current_value = getattr(category_obj, current_attr)
                setattr(category_obj, current_attr, current_value + amount)
                
                # Update category transaction details
                category_obj.transaction = detail
                category_obj.detail = detail
                category_obj.date = date
                
                db.session.commit()
                flash("Money spent successfully!", "success")
            else:
                flash("Insufficient total budget.", "error")

            return redirect(url_for('BP.budget'))

    # Prepare data for template (same as before)
    categories = {
        "Accommodation and Utilities": {
            "budget": budget.accommodation.acc_budget if budget.accommodation else 0,
            "current": budget.accommodation.acc_current if budget.accommodation else 0
        },
        "Entertainment": {
            "budget": budget.entertainment.ent_budget if budget.entertainment else 0,
            "current": budget.entertainment.ent_current if budget.entertainment else 0
        },
        "Food and Clothes": {
            "budget": budget.food.food_budget if budget.food else 0,
            "current": budget.food.food_current if budget.food else 0
        },
        "Transportation": {
            "budget": budget.transportation.trs_budget if budget.transportation else 0,
            "current": budget.transportation.trs_current if budget.transportation else 0
        },
        "Subscription": {
            "budget": budget.subscription.subs_budget if budget.subscription else 0,
            "current": budget.subscription.subs_current if budget.subscription else 0
        },
        "Others": {
            "budget": budget.other.other_budget if budget.other else 0,
            "current": budget.other.other_current if budget.other else 0
        }
    }

    category_labels = list(categories.keys())
    category_values = [cat["current"] or 0 for cat in categories.values()]

    if not any(category_values):
        category_labels = ["No Data"]
        category_values = [1]

    return render_template(
        'budget.html',
        total_budget=budget.curr_total_budget or 0,
        categories=categories,
        category_labels=category_labels,
        category_values=category_values
    )
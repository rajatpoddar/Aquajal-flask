from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory data storage (replace with a database in a real app)
data = {
    "trips": [],
    "sales": [],
    "expenses": []
}

# --- Driver Routes ---

@app.route('/driver', methods=['GET', 'POST'])
def driver_dashboard():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'trip':
            jars = int(request.form.get('jars'))
            data['trips'].append({'date': datetime.now(), 'jars': jars})

        elif form_type == 'sale':
            item = request.form.get('item')
            quantity = int(request.form.get('quantity'))
            price = 150 if item in ['New Jar', 'Dispenser'] else 15
            amount = price * quantity
            data['sales'].append({'date': datetime.now(), 'item': item, 'quantity': quantity, 'amount': amount})

        elif form_type == 'expense':
            expense_type = request.form.get('expense_type')
            amount = float(request.form.get('amount'))
            data['expenses'].append({'date': datetime.now(), 'type': expense_type, 'amount': amount})

        return redirect(url_for('driver_dashboard'))

    return render_template('driver.html', data=data)

# --- Manager Routes ---

@app.route('/manager')
def manager_dashboard():
    # Calculate daily and monthly stats
    today = datetime.now().date()
    current_month = datetime.now().month

    daily_stats = {
        'jars_sold': sum(s['quantity'] for s in data['sales'] if s['date'].date() == today and s['item'] == 'Jar'),
        'revenue': sum(s['amount'] for s in data['sales'] if s['date'].date() == today),
        'expenses': sum(e['amount'] for e in data['expenses'] if e['date'].date() == today),
        'trips': len([t for t in data['trips'] if t['date'].date() == today])
    }
    daily_stats['profit'] = daily_stats['revenue'] - daily_stats['expenses']

    monthly_stats = {
        'jars_sold': sum(s['quantity'] for s in data['sales'] if s['date'].month == current_month and s['item'] == 'Jar'),
        'revenue': sum(s['amount'] for s in data['sales'] if s['date'].month == current_month),
        'expenses': sum(e['amount'] for e in data['expenses'] if e['date'].month == current_month),
        'trips': len([t for t in data['trips'] if t['date'].month == current_month])
    }
    monthly_stats['profit'] = monthly_stats['revenue'] - monthly_stats['expenses']

    return render_template('manager.html', daily=daily_stats, monthly=monthly_stats, all_data=data)


if __name__ == '__main__':
    app.run(debug=True)
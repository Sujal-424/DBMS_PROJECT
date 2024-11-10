from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)

class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Measure(db.Model):
    measure_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id'), primary_key=True)
    measure_id = db.Column(db.Integer, db.ForeignKey('measure.measure_id'))
    amount = db.Column(db.Integer)

@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe_ingredients = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()
    ingredients = [
        {
            'name': Ingredient.query.get(ri.ingredient_id).name,
            'amount': ri.amount,
            'measure': Measure.query.get(ri.measure_id).name
        }
        for ri in recipe_ingredients
    ]
    return render_template('recipe_detail.html', recipe=recipe, ingredients=ingredients)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        
        recipe = Recipe(name=name, description=description, instructions=instructions)
        db.session.add(recipe)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('add_recipe.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

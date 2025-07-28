# food_calaries.py:
# 50 food items with calorie values (per gram, per ml, or per item/slice as noted by 'input_unit')
FOOD_CALORIES_DATABASE = {
    "apple": [{"input_unit": "item", "calories_per_input_unit": 95}],
    "banana": [{"input_unit": "item", "calories_per_input_unit": 105}],
    "orange": [{"input_unit": "item", "calories_per_input_unit": 62}],
    "pear": [{"input_unit": "item", "calories_per_input_unit": 100}],
    "grapes": [{"input_unit": "gram", "calories_per_input_unit": 0.69}], # 69 kcal/100g -> 0.69 kcal/gram
    "strawberry": [{"input_unit": "gram", "calories_per_input_unit": 0.32}], # 32 kcal/100g -> 0.32 kcal/gram
    "blueberry": [{"input_unit": "gram", "calories_per_input_unit": 0.57}], # 57 kcal/100g -> 0.57 kcal/gram
    "watermelon": [{"input_unit": "gram", "calories_per_input_unit": 0.30}], # 30 kcal/100g -> 0.30 kcal/gram
    "pineapple": [{"input_unit": "gram", "calories_per_input_unit": 0.50}], # 50 kcal/100g -> 0.50 kcal/gram
    "kiwi": [{"input_unit": "item", "calories_per_input_unit": 42}],
    "mango": [{"input_unit": "item", "calories_per_input_unit": 150}],
    "peach": [{"input_unit": "item", "calories_per_input_unit": 59}],
    "plum": [{"input_unit": "item", "calories_per_input_unit": 30}],
    "cherry": [{"input_unit": "gram", "calories_per_input_unit": 0.50}], # 50 kcal/100g -> 0.50 kcal/gram
    "apricot": [{"input_unit": "item", "calories_per_input_unit": 17}],
    "carrot": [{"input_unit": "gram", "calories_per_input_unit": 0.41}], # 41 kcal/100g -> 0.41 kcal/gram
    "potato": [{"input_unit": "gram", "calories_per_input_unit": 0.77}], # 77 kcal/100g -> 0.77 kcal/gram
    "tomato": [{"input_unit": "item", "calories_per_input_unit": 22}],
    "cucumber": [{"input_unit": "gram", "calories_per_input_unit": 0.16}], # 16 kcal/100g -> 0.16 kcal/gram
    "lettuce": [{"input_unit": "gram", "calories_per_input_unit": 0.15}], # 15 kcal/100g -> 0.15 kcal/gram
    "broccoli": [{"input_unit": "gram", "calories_per_input_unit": 0.34}], # 34 kcal/100g -> 0.34 kcal/gram
    "cauliflower": [{"input_unit": "gram", "calories_per_input_unit": 0.25}], # 25 kcal/100g -> 0.25 kcal/gram
    "spinach": [{"input_unit": "gram", "calories_per_input_unit": 0.23}], # 23 kcal/100g -> 0.23 kcal/gram
    "onion": [{"input_unit": "gram", "calories_per_input_unit": 0.40}], # 40 kcal/100g -> 0.40 kcal/gram
    "garlic": [{"input_unit": "clove", "calories_per_input_unit": 4}],
    "egg": [{"input_unit": "item", "calories_per_input_unit": 68}],
    "chicken breast": [{"input_unit": "gram", "calories_per_input_unit": 1.65}], # 165 kcal/100g -> 1.65 kcal/gram
    "beef": [{"input_unit": "gram", "calories_per_input_unit": 2.50}], # 250 kcal/100g -> 2.50 kcal/gram
    "lamb": [{"input_unit": "gram", "calories_per_input_unit": 2.94}], # 294 kcal/100g -> 2.94 kcal/gram
    "salmon": [{"input_unit": "gram", "calories_per_input_unit": 2.08}], # 208 kcal/100g -> 2.08 kcal/gram
    "tuna": [{"input_unit": "gram", "calories_per_input_unit": 1.32}], # 132 kcal/100g -> 1.32 kcal/gram
    "shrimp": [{"input_unit": "gram", "calories_per_input_unit": 0.99}], # 99 kcal/100g -> 0.99 kcal/gram
    "rice": [{"input_unit": "gram", "calories_per_input_unit": 1.30}], # 130 kcal/100g -> 1.30 kcal/gram
    "bread": [{"input_unit": "slice", "calories_per_input_unit": 80}],
    "pasta": [{"input_unit": "gram", "calories_per_input_unit": 1.31}], # 131 kcal/100g -> 1.31 kcal/gram
    "pizza": [{"input_unit": "slice", "calories_per_input_unit": 285}],
    "hamburger": [{"input_unit": "item", "calories_per_input_unit": 250}],
    "hot dog": [{"input_unit": "item", "calories_per_input_unit": 150}],
    "cheese": [{"input_unit": "gram", "calories_per_input_unit": 4.02}], # 402 kcal/100g -> 4.02 kcal/gram
    "milk": [{"input_unit": "ml", "calories_per_input_unit": 0.51}], # 122 kcal/cup (240ml) -> 122/240 = ~0.508 -> 0.51 kcal/ml
    "yogurt": [{"input_unit": "cup", "calories_per_input_unit": 59}],
    "butter": [{"input_unit": "tbsp", "calories_per_input_unit": 102}],
    "olive oil": [{"input_unit": "tbsp", "calories_per_input_unit": 119}],
    "sugar": [{"input_unit": "tsp", "calories_per_input_unit": 16}],
    "honey": [{"input_unit": "tbsp", "calories_per_input_unit": 64}],
    "almonds": [{"input_unit": "nut", "calories_per_input_unit": 7}], # 70 kcal/10 nuts -> 7 kcal/nut
    "walnuts": [{"input_unit": "half", "calories_per_input_unit": 9.8}], # 98 kcal/10 halves -> 9.8 kcal/half
    "peanut butter": [{"input_unit": "tbsp", "calories_per_input_unit": 94}],
    "potato chips": [{"input_unit": "gram", "calories_per_input_unit": 5.43}], # 152 kcal/28g -> 5.428 -> 5.43 kcal/gram
    "chocolate": [{"input_unit": "piece", "calories_per_input_unit": 50}],
    "ice cream": [{"input_unit": "scoop", "calories_per_input_unit": 137}],
    "cookie": [{"input_unit": "item", "calories_per_input_unit": 78}],
    "cake": [{"input_unit": "slice", "calories_per_input_unit": 235}],
}
# food_calaries.py:
# Food items with various unit options, calorie values, and input properties.
FOOD_CALORIES_DATABASE = {
    "apple": [
        {"unit_name": "item", "calories_per_unit_value": 95, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "banana": [
        {"unit_name": "item", "calories_per_unit_value": 105, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "orange": [
        {"unit_name": "item", "calories_per_unit_value": 62, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "pear": [
        {"unit_name": "item", "calories_per_unit_value": 100, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "grapes": [
        {"unit_name": "gram", "calories_per_unit_value": 0.69, "is_discrete_input": False, "default_quantity_input": 100}, # 69 kcal/100g
        {"unit_name": "cup", "calories_per_unit_value": 104, "is_discrete_input": False, "default_quantity_input": 1}, # ~150g * 0.69
    ],
    "strawberry": [
        {"unit_name": "gram", "calories_per_unit_value": 0.32, "is_discrete_input": False, "default_quantity_input": 100}, # 32 kcal/100g
        {"unit_name": "item", "calories_per_unit_value": 5, "is_discrete_input": True, "default_quantity_input": 10}, # ~15g per item
    ],
    "blueberry": [
        {"unit_name": "gram", "calories_per_unit_value": 0.57, "is_discrete_input": False, "default_quantity_input": 100}, # 57 kcal/100g
        {"unit_name": "cup", "calories_per_unit_value": 85, "is_discrete_input": False, "default_quantity_input": 1}, # ~148g * 0.57
    ],
    "watermelon": [
        {"unit_name": "gram", "calories_per_unit_value": 0.30, "is_discrete_input": False, "default_quantity_input": 200}, # 30 kcal/100g
        {"unit_name": "slice", "calories_per_unit_value": 150, "is_discrete_input": False, "default_quantity_input": 1}, # ~500g slice
    ],
    "pineapple": [
        {"unit_name": "gram", "calories_per_unit_value": 0.50, "is_discrete_input": False, "default_quantity_input": 100}, # 50 kcal/100g
        {"unit_name": "slice", "calories_per_unit_value": 40, "is_discrete_input": True, "default_quantity_input": 1}, # ~80g slice
    ],
    "kiwi": [
        {"unit_name": "item", "calories_per_unit_value": 42, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "mango": [
        {"unit_name": "item", "calories_per_unit_value": 150, "is_discrete_input": True, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 0.60, "is_discrete_input": False, "default_quantity_input": 250}, # ~250g per mango
    ],
    "peach": [
        {"unit_name": "item", "calories_per_unit_value": 59, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "plum": [
        {"unit_name": "item", "calories_per_unit_value": 30, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "cherry": [
        {"unit_name": "gram", "calories_per_unit_value": 0.50, "is_discrete_input": False, "default_quantity_input": 50}, # 50 kcal/100g
        {"unit_name": "item", "calories_per_unit_value": 5, "is_discrete_input": True, "default_quantity_input": 10}, # ~10g per cherry
    ],
    "apricot": [
        {"unit_name": "item", "calories_per_unit_value": 17, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "carrot": [
        {"unit_name": "gram", "calories_per_unit_value": 0.41, "is_discrete_input": False, "default_quantity_input": 100}, # 41 kcal/100g
        {"unit_name": "item", "calories_per_unit_value": 20, "is_discrete_input": True, "default_quantity_input": 1}, # ~50g per carrot
    ],
    "potato": [
        {"unit_name": "gram", "calories_per_unit_value": 0.77, "is_discrete_input": False, "default_quantity_input": 150}, # 77 kcal/100g
        {"unit_name": "item (medium)", "calories_per_unit_value": 170, "is_discrete_input": True, "default_quantity_input": 1}, # ~220g potato
    ],
    "tomato": [
        {"unit_name": "item", "calories_per_unit_value": 22, "is_discrete_input": True, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 0.18, "is_discrete_input": False, "default_quantity_input": 100}, # ~120g per tomato
    ],
    "cucumber": [
        {"unit_name": "gram", "calories_per_unit_value": 0.16, "is_discrete_input": False, "default_quantity_input": 100}, # 16 kcal/100g
    ],
    "lettuce": [
        {"unit_name": "gram", "calories_per_unit_value": 0.15, "is_discrete_input": False, "default_quantity_input": 50}, # 15 kcal/100g
    ],
    "broccoli": [
        {"unit_name": "gram", "calories_per_unit_value": 0.34, "is_discrete_input": False, "default_quantity_input": 100}, # 34 kcal/100g
        {"unit_name": "cup (chopped)", "calories_per_unit_value": 31, "is_discrete_input": False, "default_quantity_input": 1}, # ~90g per cup
    ],
    "cauliflower": [
        {"unit_name": "gram", "calories_per_unit_value": 0.25, "is_discrete_input": False, "default_quantity_input": 100}, # 25 kcal/100g
        {"unit_name": "cup (chopped)", "calories_per_unit_value": 27, "is_discrete_input": False, "default_quantity_input": 1}, # ~100g per cup
    ],
    "spinach": [
        {"unit_name": "gram", "calories_per_unit_value": 0.23, "is_discrete_input": False, "default_quantity_input": 50}, # 23 kcal/100g
        {"unit_name": "cup (raw)", "calories_per_unit_value": 7, "is_discrete_input": False, "default_quantity_input": 2}, # ~30g per cup
    ],
    "onion": [
        {"unit_name": "gram", "calories_per_unit_value": 0.40, "is_discrete_input": False, "default_quantity_input": 50}, # 40 kcal/100g
        {"unit_name": "item (medium)", "calories_per_unit_value": 45, "is_discrete_input": True, "default_quantity_input": 1}, # ~110g per medium onion
    ],
    "garlic": [
        {"unit_name": "clove", "calories_per_unit_value": 4, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "egg": [
        {"unit_name": "item", "calories_per_unit_value": 68, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "chicken breast": [
        {"unit_name": "gram", "calories_per_unit_value": 1.65, "is_discrete_input": False, "default_quantity_input": 150}, # 165 kcal/100g
        {"unit_name": "serving (100g)", "calories_per_unit_value": 165, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "beef": [
        {"unit_name": "gram", "calories_per_unit_value": 2.50, "is_discrete_input": False, "default_quantity_input": 150}, # 250 kcal/100g
        {"unit_name": "serving (100g)", "calories_per_unit_value": 250, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "lamb": [
        {"unit_name": "gram", "calories_per_unit_value": 2.94, "is_discrete_input": False, "default_quantity_input": 150}, # 294 kcal/100g
        {"unit_name": "serving (100g)", "calories_per_unit_value": 294, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "salmon": [
        {"unit_name": "gram", "calories_per_unit_value": 2.08, "is_discrete_input": False, "default_quantity_input": 150}, # 208 kcal/100g
        {"unit_name": "fillet (170g)", "calories_per_unit_value": 354, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "tuna": [
        {"unit_name": "gram", "calories_per_unit_value": 1.32, "is_discrete_input": False, "default_quantity_input": 100}, # 132 kcal/100g
        {"unit_name": "can (drained 85g)", "calories_per_unit_value": 112, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "shrimp": [
        {"unit_name": "gram", "calories_per_unit_value": 0.99, "is_discrete_input": False, "default_quantity_input": 100}, # 99 kcal/100g
        {"unit_name": "piece (medium)", "calories_per_unit_value": 10, "is_discrete_input": True, "default_quantity_input": 10}, # ~10g per piece
    ],
    "rice": [
        {"unit_name": "gram", "calories_per_unit_value": 1.30, "is_discrete_input": False, "default_quantity_input": 100}, # 130 kcal/100g
        {"unit_name": "cup (cooked)", "calories_per_unit_value": 195, "is_discrete_input": False, "default_quantity_input": 1}, # ~150g cooked rice
    ],
    "bread": [
        {"unit_name": "slice", "calories_per_unit_value": 80, "is_discrete_input": True, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 2.6, "is_discrete_input": False, "default_quantity_input": 30}, # ~30g per slice
    ],
    "pasta": [
        {"unit_name": "gram", "calories_per_unit_value": 1.31, "is_discrete_input": False, "default_quantity_input": 100}, # 131 kcal/100g
        {"unit_name": "cup (cooked)", "calories_per_unit_value": 180, "is_discrete_input": False, "default_quantity_input": 1}, # ~140g cooked pasta
    ],
    "pizza": [
        {"unit_name": "slice", "calories_per_unit_value": 285, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "hamburger": [
        {"unit_name": "item", "calories_per_unit_value": 250, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "hot dog": [
        {"unit_name": "item", "calories_per_unit_value": 150, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "cheese": [
        {"unit_name": "gram", "calories_per_unit_value": 4.02, "is_discrete_input": False, "default_quantity_input": 30}, # 402 kcal/100g
        {"unit_name": "slice", "calories_per_unit_value": 113, "is_discrete_input": True, "default_quantity_input": 1}, # ~28g slice
    ],
    "milk": [
        {"unit_name": "ml", "calories_per_unit_value": 0.51, "is_discrete_input": False, "default_quantity_input": 200}, # 122 kcal/cup (~240ml)
        {"unit_name": "cup", "calories_per_unit_value": 122, "is_discrete_input": False, "default_quantity_input": 1},
    ],
    "yogurt": [
        {"unit_name": "cup", "calories_per_unit_value": 59, "is_discrete_input": False, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 0.59, "is_discrete_input": False, "default_quantity_input": 100}, # 59 kcal/100g (approx 1 cup)
    ],
    "butter": [
        {"unit_name": "tbsp", "calories_per_unit_value": 102, "is_discrete_input": False, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 7.17, "is_discrete_input": False, "default_quantity_input": 10}, # ~14.2g per tbsp
    ],
    "olive oil": [
        {"unit_name": "tbsp", "calories_per_unit_value": 119, "is_discrete_input": False, "default_quantity_input": 1},
        {"unit_name": "ml", "calories_per_unit_value": 9, "is_discrete_input": False, "default_quantity_input": 15}, # ~13.5g per tbsp, ~0.9 kcal/g -> 9 kcal/ml
    ],
    "sugar": [
        {"unit_name": "tsp", "calories_per_unit_value": 16, "is_discrete_input": False, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 3.87, "is_discrete_input": False, "default_quantity_input": 5}, # ~4g per tsp
    ],
    "honey": [
        {"unit_name": "tbsp", "calories_per_unit_value": 64, "is_discrete_input": False, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 3.04, "is_discrete_input": False, "default_quantity_input": 15}, # ~21g per tbsp
    ],
    "almonds": [
        {"unit_name": "nut", "calories_per_unit_value": 7, "is_discrete_input": True, "default_quantity_input": 10}, # 70 kcal/10 nuts
        {"unit_name": "gram", "calories_per_unit_value": 5.75, "is_discrete_input": False, "default_quantity_input": 10}, # 575 kcal/100g
    ],
    "walnuts": [
        {"unit_name": "half", "calories_per_unit_value": 9.8, "is_discrete_input": True, "default_quantity_input": 10}, # 98 kcal/10 halves
        {"unit_name": "gram", "calories_per_unit_value": 6.54, "is_discrete_input": False, "default_quantity_input": 10}, # 654 kcal/100g
    ],
    "peanut butter": [
        {"unit_name": "tbsp", "calories_per_unit_value": 94, "is_discrete_input": False, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 5.88, "is_discrete_input": False, "default_quantity_input": 15}, # ~16g per tbsp
    ],
    "potato chips": [
        {"unit_name": "gram", "calories_per_unit_value": 5.43, "is_discrete_input": False, "default_quantity_input": 30}, # 152 kcal/28g
        {"unit_name": "bag (28g)", "calories_per_unit_value": 152, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "chocolate": [
        {"unit_name": "piece", "calories_per_unit_value": 50, "is_discrete_input": True, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 5.35, "is_discrete_input": False, "default_quantity_input": 10}, # 535 kcal/100g
    ],
    "ice cream": [
        {"unit_name": "scoop", "calories_per_unit_value": 137, "is_discrete_input": True, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 2.07, "is_discrete_input": False, "default_quantity_input": 100}, # 207 kcal/100g
    ],
    "cookie": [
        {"unit_name": "item", "calories_per_unit_value": 78, "is_discrete_input": True, "default_quantity_input": 1},
    ],
    "cake": [
        {"unit_name": "slice", "calories_per_unit_value": 235, "is_discrete_input": True, "default_quantity_input": 1},
        {"unit_name": "gram", "calories_per_unit_value": 3.75, "is_discrete_input": False, "default_quantity_input": 50}, # 375 kcal/100g
    ],
}
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client (assuming API key is in the environment)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Function to check if a product is suitable based on allergens
def is_product_suitable(product_name: str, product_ingredients: list, user_allergens: list) -> str:
    """
    Uses Groq API (Llama model) to check if a product is safe for a user based on allergens.
    """
    prompt = f"""
    You are a food safety expert. Your task is to check if a product is safe for a user based on their allergens.
    
    Product Name: {product_name}
    Ingredients: {", ".join(product_ingredients)}
    User Allergens: {", ".join(user_allergens)}
    
    Instructions:
    - Identify if any ingredient in the product matches or is related to any allergen listed.
    - If any allergen is present, respond with: "No"
    - If the product is safe, respond with: "Yes"
    - Only return "Yes" or "No". Do not provide any explanation.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",  # Choose the model you prefer
    )
    
    answer = chat_completion.choices[0].message.content.strip()
    return answer


# Function to get product recommendations based on a user's profile
def get_product_recommendations(failed_product_name: str, category_products: dict, user_allergens: list, num_recommendations: int = 3) -> str:
    """
    Requests product recommendations based on a user's allergens and the failed product.
    """
    prompt = f"""
    The following product failed the allergen suitability check for a user:

    Failed Product: {failed_product_name}
    
    User Allergens: {", ".join(user_allergens)}

    Instructions:
    - Based on the failed product, recommend {num_recommendations} other products from the same category.
    - The products you recommend must not contain any of the allergens listed.
    - For each recommended product, include its name only if it is safe (i.e., does not contain any allergens).
    - Respond with the names of suitable products only. Limit the list to {num_recommendations} products.
    """
    
    category_products_str = "\n".join([f"{product_name}: {', '.join(ingredients)}" for product_name, ingredients in category_products.items()])
    
    prompt += f"\n\nList of products in the same category:\n{category_products_str}"

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",  
    )
    
    recommendations = chat_completion.choices[0].message.content.strip()
    return recommendations


# Example 1: Check if a product is safe for a user based on their allergens
product_name = "Vegan Protein Shake"
product_ingredients = ["pea protein", "brown rice syrup", "flaxseed", "almond milk"]
user_allergens = ["milk", "soy"]

suitability = is_product_suitable(product_name, product_ingredients, user_allergens)
print(f"Suitability of {product_name}: {suitability}")  # Expected output: "Yes" (since it's vegan and allergen-free for this user)

# Example 2: Get product recommendations for a user based on their profile and allergens
failed_product_name = "Vegan Protein Shake"  # The product that failed the suitability check
category_products = {
    "Product A": ["water", "sugar", "corn starch"],
    "Product B": ["milk", "sugar", "corn starch"],
    "Product C": ["water", "sugar", "gluten-free flour", "almond milk"],
    "Product D": ["coconut milk", "sugar", "gluten-free flour"]
}
user_allergens = ["milk", "soy", "nuts"]

recommendations = get_product_recommendations(failed_product_name, category_products, user_allergens, num_recommendations=3)
print(f"Recommended Products: {recommendations}")  # List of recommended products

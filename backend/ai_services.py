import os
from groq import Groq
from dotenv import load_dotenv
from db_session import get_db
from database.commands_database import add_shopping_cart, get_product_by_category_without_blacklisted, get_client, get_shopping_cart_items, get_product, add_recommendations
from websocket_manager import notify_client
import asyncio

load_dotenv()

# Initialize Groq client (assuming API key is in the environment)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#TODO-Meal Recommendation

def add_product_use_ai(product, uid):
    db = next(get_db())
    user = get_client(db, 1)
    product = get_product(db, product.id)
    response = is_product_suitable(product.name, product.ingredients, user.allergens)
    success = (response == "Yes")
    if not success:
        try:
            recommendations = get_product_recommendations(product, get_product_by_category_without_blacklisted(db, product.category_id, product.id), user.allergens)
            rec = [int(x) for x in recommendations.split(", ")]
            for recommendation in rec:
                add_recommendations(db, 1, product.id, recommendation)
            print(recommendations)
            
        except Exception as e:
            print(e)
            print("No recommendations")
    add_shopping_cart(db, 1, product.id, uid, success)
    asyncio.run(notify_client("1", "ADD")) 
    for item in get_shopping_cart_items(db, 1):
        print(item.product.name)
    
    
# Function to check if a product is suitable based on allergens
def is_product_suitable(product_name: str, product_ingredients: list, user_allergens: list) -> str:
    """
    Uses Groq API (Llama model) to check if a product is safe for a user based on allergens.
    """
    prompt = f"""
    You are a food safety expert. Your task is to check if a product is safe for a user based on their allergens.
    
    Product Name: {product_name}
    Ingredients: {", ".join([ingredient.name for ingredient in product_ingredients])}
    User Allergens: {", ".join([allergen.name for allergen in user_allergens])}
    
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
def get_product_recommendations(failed_product, category_products, user_allergens: list, num_recommendations: int = 10) -> str:
    """
    Requests product recommendations based on a user's allergens and the failed product.
    """
    prompt = f"""
    The following product failed the allergen suitability check for a user:

    Failed Product: {failed_product.name}
    
    User Allergens: {", ".join([allergen.name for allergen in user_allergens])}
    Instructions:
    - Based on the failed product, recommend {num_recommendations} other products from the same category.
    - The products you recommend must not contain any of the allergens listed.
    - For each recommended product, include its id only if it is safe (i.e., does not contain any allergens).
    - Respond with the ids of suitable products only. Limit the list to {num_recommendations} products.
    """
    category_products_str = "\n".join([f"{product.id}: {", ".join([ingredient.name for ingredient in product.ingredients])}" for product in category_products])
    
    prompt += f"\n\nList of products in the same category:\n{category_products_str}"

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",  
    )
    
    recommendations = chat_completion.choices[0].message.content.strip()    
    print(recommendations)          
    return recommendations

#!/bin/env python3

"""This script allows users to ask the AI for ingredients of a specific food, check if an ingredient is in a dish, or analyze the properties of a food item, including analyzing an image of the food item."""

import json
import os
import re
import sys
import readline
from PIL import Image
import google.generativeai as genai
from google.api_core import exceptions
import streamlit as st
import requests
import io

def initialize_genai():
    """Initialize the generative AI module and configure it."""

    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(script_dir, "keys.json")

        with open(file, "r", encoding="utf-8") as f:
            content = json.load(f)
            gemini_api_key = content["GEMINI_API_KEY"]

            if gemini_api_key == "your gemini api key here":
                print("To use the Gemini API, you'll need an API key.")
                print("Create a key in Google AI Studio.")
                print("Save the key to 'keys.json' file.")

                sys.exit(1)

            gemini_model = content["GEMINI_MODEL"]
            safety_settings = content["SAFETY_SETTINGS"]
            generation_config = content["GENERATION_CONFIG"]

            genai.configure(api_key=gemini_api_key)

    except FileNotFoundError:
        print("Could not find the configuration file 'keys.json'. Ensure it exists")
        sys.exit(1)

    except json.JSONDecodeError:
        print("Error: Could not parse the key file 'keys.json'. Please check the file format.")
        sys.exit(1)

    except KeyError as e:
        print(f"Error: Missing key '{e.args[0]}' in 'keys.json' file.")
        sys.exit(1)

    model = genai.GenerativeModel(
        model_name=gemini_model,
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    return model

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def get_gemini_response(input_prompt, image_data, user_input):
    """Send the image data and user input to Gemini AI for analysis."""
    # Placeholder for actual interaction with Gemini AI
    # Assuming this function processes the image data and generates a response
    return "This is a placeholder response for the Gemini AI analysis."

def analyze_image_with_gemini(model, image_path):
    """Analyze the input image using Gemini AI and extract relevant information."""
    try:
        # Open the image from the local path
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Send the image to Gemini AI for analysis
        response = model.start_chat(history=[]).send_message(
            message="Analyze this image for food information.",
            images=[content]
        )
        return response.text

    except FileNotFoundError:
        print("Error: The specified image file could not be found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred while analyzing the image: {e}")
        return None

def food_ingredients_chat():
    """Input: food name  ->  output: ingredients, check if an ingredient is in the dish, or analyze the properties of a food item."""
    print("You are using the Food Ingredients Model.")
    model = initialize_genai()
    chat = model.start_chat(history=[])

    last_food_item = None
    last_dish_description = None

    while True:
        print("Options:")
        print("1. Get ingredients of a food item.")
        print("2. Check if an ingredient is in a dish.")
        print("3. Analyze the properties of a food item.")
        option = input("Choose an option (1, 2, or 3): ")

        if option == "1":
            if last_food_item:
                use_last = input(f"Use the last analyzed food item '{last_food_item}'? (yes/no): ")
                if use_last.lower() == "yes":
                    food_item = last_food_item
                else:
                    food_item = input("Enter a food to get its ingredients: ")
            else:
                food_item = input("Enter a food to get its ingredients: ")

            if food_item == "" or food_item.isspace():
                print("The food item is empty. Please try again.\n")
                continue

            try:
                query = f"What are the detailed and specific ingredients of {food_item}? Include any sub-ingredients and specific types of ingredients used."
                response = chat.send_message(query, stream=False)
                print("Ingredients: ")
                print(response.text)

            except exceptions.DeadlineExceeded as error:
                print("Deadline exceeded (Internet connection could be lost)")
                print(error.message, "\n")
                continue

            except exceptions.InvalidArgument as error:
                print("Request fails API validation or you tried to access a model that requires allowlisting.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.PermissionDenied as error:
                print("Client doesn't have sufficient permission to call the API.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.NotFound as error:
                print("No valid object is found from the designated URL.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.ResourceExhausted as error:
                print("API quota over the limit or server overload.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.Unknown as error:
                print("Server error due to overload or dependency failure.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.ServiceUnavailable as error:
                print("Service is temporarily unavailable.")
                print(error.message, "\n")
                sys.exit(1)

        elif option == "2":
            if last_food_item:
                use_last = input(f"Use the last analyzed dish '{last_food_item}'? (yes/no): ")
                if use_last.lower() == "yes":
                    dish = last_food_item
                else:
                    dish = input("Enter the name of the dish: ")
            else:
                dish = input("Enter the name of the dish: ")

            ingredient = input("Enter the ingredient to check: ")

            if dish == "" or dish.isspace() or ingredient == "" or ingredient.isspace():
                print("Dish or ingredient input is empty. Please try again.\n")
                continue

            try:
                query = f"Does {dish} contain {ingredient}? Provide detailed information on how this ingredient is used in the dish if present."
                response = chat.send_message(query, stream=False)
                print("Response: ")
                print(response.text)

            except exceptions.DeadlineExceeded as error:
                print("Deadline exceeded (Internet connection could be lost)")
                print(error.message, "\n")
                continue

            except exceptions.InvalidArgument as error:
                print("Request fails API validation or you tried to access a model that requires allowlisting.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.PermissionDenied as error:
                print("Client doesn't have sufficient permission to call the API.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.NotFound as error:
                print("No valid object is found from the designated URL.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.ResourceExhausted as error:
                print("API quota over the limit or server overload.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.Unknown as error:
                print("Server error due to overload or dependency failure.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.ServiceUnavailable as error:
                print("Service is temporarily unavailable.")
                print(error.message, "\n")
                sys.exit(1)

        elif option == "3":
            food_item = input("Enter the name of the food item: ")
            description = input("Enter a description of the food item: ")
            image = input("Enter the local path of the food item image (optional): ")

            if food_item == "" or food_item.isspace():
                print("The food item is empty. Please try again.\n")
                continue

            if image:
                extracted_text = analyze_image_with_gemini(model, image)
                if extracted_text:
                    description += f" {extracted_text}"

            try:
                query = (
                    f"Analyze the food item '{food_item}'. {description}. "
                    f"Does it contain meat, seafood, red meat, poultry, other meat, eggs, dairy, honey, seafood, milk, fish, shellfish, tree nuts, peanuts, soy? "
                    f"Provide the response as '1' for yes and '0' for no. "
                    f"Also, indicate if it is high, medium, or low in wheat, gluten, lactose, paleo, sugar, carbs, protein, fat, calories."
                )
                response = chat.send_message(query, stream=False)
                print("Analysis: ")
                print(response.text)
                last_food_item = food_item
                last_dish_description = description

            except exceptions.DeadlineExceeded as error:
                print("Deadline exceeded (Internet connection could be lost)")
                print(error.message, "\n")
                continue

            except exceptions.InvalidArgument as error:
                print("Request fails API validation or you tried to access a model that requires allowlisting.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.PermissionDenied as error:
                print("Client doesn't have sufficient permission to call the API.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.NotFound as error:
                print("No valid object is found from the designated URL.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.ResourceExhausted as error:
                print("API quota over the limit or server overload.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.Unknown as error:
                print("Server error due to overload or dependency failure.")
                print(error.message, "\n")
                sys.exit(1)

            except exceptions.ServiceUnavailable as error:
                print("Service is temporarily unavailable.")
                print(error.message, "\n")
                sys.exit(1)

        else:
            print("Invalid option. Please enter 1, 2, or 3.\n")

def main():
    """Main logic of the script."""
    os.system("clear -x")

    if len(sys.argv) > 1:
        print(f"Error: Unknown argument: {sys.argv[1]}")
        sys.exit(1)

    food_ingredients_chat()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("___ See ya! ___")
        sys.exit(0)

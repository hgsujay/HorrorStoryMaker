from story import Story


story = Story()
story_id = ""

# prompt for regnerating images
print("Do you want to regenerate images? (Y/N)")
user_input = input()
while user_input.lower() == "y":
    print("Enter the paragraph number to regenerate images")
    order = input()
    if order.isdigit():
        order = int(order)
        print("Enter the new prompt for generating the image")
        prompt_override = input()
        story.regenerate_images(order, prompt_override)
    print("Do you want to regenerate images? (Y/N)")
    user_input = input()

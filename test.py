from PIL import Image, ImageDraw

def ImageDimensions(width_inches, height_inches):
    dpi = 200
    width_pixels = int(width_inches * dpi)
    height_pixels = int(height_inches * dpi)
    # print(width_pixels, height_pixels)
    return (width_pixels, height_pixels)

def draw_boxes_grid(dimensions, box_size, margin, boxes_per_row, num_boxes, fuel):
    """
    Draws a grid of small boxes on a new image.

    :param image_width: Total width of the output image.
    :param image_height: Total height of the output image.
    :param box_size: The width and height of each individual box.
    :param margin: The space between boxes and from the edges.
    :param boxes_per_row: The number of boxes to draw before moving to the next row.
    :param num_boxes: The total number of boxes to draw.
    """
    # Create a new image
    image = Image.new('RGB', dimensions, color='white')
    draw = ImageDraw.Draw(image)

    # Starting coordinates for the first box
    current_x = 490
    current_y = 299

    for i in range(num_boxes):
        # Calculate the coordinates for the current box (top-left and bottom-right)
        x0 = current_x
        y0 = current_y
        x1 = current_x + box_size
        y1 = current_y + box_size
        
        # Ensure the box fits within the image boundary, otherwise skip
        if (i+1) > fuel:
            draw.rectangle([(x0, y0), (x1, y1)], outline='black', fill='grey')
        else:
            draw.rectangle([(x0, y0), (x1, y1)], outline='black', fill='white')

        # Check if four boxes have been drawn in the current row (using modulo)
        if (i + 1) % boxes_per_row == 0:
            # Move to the next row: reset x and increment y
            current_x = 490
            current_y += box_size + margin
        else:
            # Stay on the same row: increment x
            current_x += box_size + margin
            
    # Save or display the image
    image.save('output_boxes_grid.png')
    image.show()

# --- Example Usage ---
# Define parameters
IMG_WIDTH = 600
IMG_HEIGHT = 400
BOX_SIZE = 10
MARGIN = 2
BOXES_PER_ROW = 4
TOTAL_BOXES = 8
FUEL = 5 


CardWidth = 3.5
CardHeight = 2.5
ImageDimensions(CardWidth,CardHeight)

# Run the function
draw_boxes_grid(ImageDimensions(CardWidth,CardHeight), BOX_SIZE, MARGIN, BOXES_PER_ROW, TOTAL_BOXES, FUEL)

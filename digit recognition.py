# import modules
import pygame
import cv2
import csv
from sklearn.neighbors import KNeighborsClassifier

pygame.init()
# Create surfaces and display
screen = pygame.display.set_mode((600, 600))
canvas = pygame.Surface((555, 405))
new_res_canvas = pygame.Surface((28, 28))
clock = pygame.time.Clock()

# Variables for design
red = [255, 0, 0]
black = [0, 0, 0]
white = [255, 255, 255]
blue = [0, 204, 204]
rect_size = 30
font = pygame.font.SysFont('bahnschrift', 30)

# load images
checkpng = pygame.image.load("Buttons/checkbutton.png")
clearpng = pygame.image.load("Buttons/clearbutton.png")
iconimg = pygame.image.load("Images/Icon -- Brush.png")
pygame.display.set_caption('Digit Recogniser')
pygame.display.set_icon(iconimg)
# Lists
pos_draw_list = []
labels = []
samples = []

# filling the surfaces
screen.fill(blue)
screen.fill(black, (20, 20, 555, 410))
screen.fill(black, (20, 450, 270, 135))
canvas.fill(black)

# read file
with open("mnist_train.csv") as file:
    reading = csv.reader(file)
    excel_file = list(reading)
    for row in excel_file:
        labels.append(int(row[0]))
        samples.append(list(map(int, row[1:])))


def changing_picture_res():
    pygame.image.save(canvas, 'Images/digit_large.png')
    predict_img = pygame.image.load('Images/digit_large.png')
    pygame.transform.smoothscale(predict_img.convert_alpha(), (28, 28), dest_surface=new_res_canvas)
    pygame.image.save(new_res_canvas, 'Images/digit.png')


def draw_screen():
    global pos_draw_list
    pygame.draw.rect(screen, red, (20, 20, 560, 415), 5)  # canvas border
    pygame.draw.rect(screen, red, (20, 450, 275, 140), 5)  # results table border

    for x, y in pos_draw_list:  # drawing based on mouse pos stored in list
        pygame.draw.rect(screen, white, (x, y, rect_size, rect_size))
        pygame.draw.rect(canvas, white, (x, y, rect_size, rect_size))
        pygame.display.update()

    if predict_button.draw():  # pressing button conditions
        changing_picture_res()
        prediction()

    if clear_button.draw():
        screen.fill(black, (20, 20, 555, 410))  # clearing all the surfaces with digit drawing
        canvas.fill(black, (20, 20, 555, 410))
        screen.fill(black, (20, 450, 270, 135))  # clear results table
        pos_draw_list = []  # emptying mouse position


def prediction():
    img = cv2.imread('Images/digit.png', cv2.IMREAD_GRAYSCALE)  # reading the RGB values in the hand-drawn digit and
    # turning into grayscale to compare with Excel data. Note: it is stored as a 2D array.
    predict_data = []

    for line in img:  # 2D array into a 1D array
        for elements in line:
            predict_data.append(elements)

    clf = KNeighborsClassifier(3)
    clf.fit(samples, labels)
    predicted_digit = clf.predict([predict_data])[0]
    # acc = accuracy_score(labels, predicted_digit)

    display_predictions(predicted_digit)


def display_predictions(predicted_digit):
    # result_accuracy = font.render(f'Accuracy: {acc}%', False, (255, 255, 255))
    result_digit = font.render(f'Predicted: {predicted_digit}', False, (255, 255, 255))
    screen.blit(result_digit, (30, 460))
    # screen.blit(result_accuracy, (30, 500))


class Button:
    def __init__(self, x, y, image):  # finding and setting values and variables for buttons
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):  # displaying the button
        action = False
        pos_button = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos_button):  # comparing if the mouse pos has collided with the image pos
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:  # checking if the user has clicked with the
                # left button and that they have not clicked already by checking if self.clicked  == False

                self.clicked = True  # Making it so that we know that the user has clicked
                action = True
            if pygame.mouse.get_pressed()[0] == 0:  # Once they have pressed the button, we return self.clicked to False
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


# Drawing the buttons

predict_button = Button(420, 450, checkpng)
clear_button = Button(300, 450, clearpng)


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_pressed()[0]:  # if the user presses the left mouse button, and they are within the canvas
            # then we will add their mouse pos into a list.
            if 400 > event.pos[1] > 25 and 550 > event.pos[0] > 25:
                try:
                    pos_draw_list.append(event.pos)
                except AttributeError:
                    pass

    draw_screen()

    pygame.display.update()
    clock.tick(60)

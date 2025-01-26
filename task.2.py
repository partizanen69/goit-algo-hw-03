# Напишіть програму на Python, яка використовує рекурсію для створення 
# фракталу «сніжинка Коха» за умови, що користувач повинен мати можливість вказати рівень рекурсії.

import turtle
import argparse

def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)

def draw_koch_snowflake(order, size=300):
    window = turtle.Screen()
    window.bgcolor("white")
    window.title("Сніжинка Коха")

    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-size/2, size/3)
    t.pendown()

    # Малюємо 4 сторони сніжинки
    for _ in range(4):
        koch_curve(t, order, size)
        t.right(90)

    window.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Створення сніжинки Коха')
    parser.add_argument('--level', type=int, default=3, help='Рівень рекурсії (ціле число >= 0)')
    args = parser.parse_args()
    
    if args.level < 0:
        print("Рівень рекурсії має бути невід'ємним числом")
    else:
        draw_koch_snowflake(args.level)

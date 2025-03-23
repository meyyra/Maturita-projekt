import pygame
import mysql.connector
import bcrypt

USER_FILE = "users.txt"

# Nastavení připojení k databázi
DB_HOST = "dbs.spskladno.cz"
DB_USER = "student8"
DB_PASSWORD = "spsnet"
DB_NAME = "vyuka8"

def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
# funkce pro získání kategorií z databáze
def get_categories():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nazev FROM 1Akategorie")
    categories = cursor.fetchall()
    cursor.close()
    db.close()
    return categories
# funkce pro získání produktů podle kategorie z databáze
def get_products_by_category(category_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT nazev, cena FROM 1Aprodukty WHERE kategorie_id = %s", (category_id,))
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return products
# funkce pro přidání produktů do databáze
def insert_product(name, price, category_id):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO 1Aprodukty (nazev, cena, kategorie_id) VALUES (%s, %s, %s)"
    val = (name, price, category_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
# funkce pro odebrání produktů z databáze
def delete_product(product_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM 1Aprodukty WHERE nazev = %s", (product_name,))
    db.commit()
    cursor.close()
    db.close()
# funkce pro kontrolu přihlašovacích údajů
def check_login(username, password):
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                stored_username, stored_hashed_password = line.strip().split(":")
                if stored_username == username and bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
                    return True  # Přihlášení úspěšné
    except FileNotFoundError:
        return False  # Soubor neexistuje
    return False  # Nesprávné přihlášení
# získání jmen uživatelů z databáze
def get_users():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT username, points FROM 1Ausers")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users
# získání bodů uživatelů z databáze
def update_user_points(username, change):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE 1Ausers SET points = points + %s WHERE username = %s", (change, username))
    db.commit()
    cursor.close()
    db.close()


#hlavní smyčka
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Kavárna S Radostí")
    font = pygame.font.Font(None, 32)
    font2 = pygame.font.Font(None, 42)
    clock = pygame.time.Clock()

    login_mode = True  # Přihlašovací režim
    login_box_user = pygame.Rect(300, 200, 200, 32)
    login_box_pass = pygame.Rect(300, 260, 200, 32)
    login_button = pygame.Rect(350, 320, 110, 40)
    user_text = ''
    pass_text = ''
    active_user = False
    active_pass = False
    login_error = False


    categories = get_categories()
    users = get_users()
    selected_category = 0
    dropdown_open = False
    products = []
    view_mode = "input"

    input_box_name = pygame.Rect(220, 100, 300, 32)
    input_box_price = pygame.Rect(220, 165, 300, 32)
    category_box = pygame.Rect(220, 230, 300, 32)
    button_box = pygame.Rect(220, 550, 100, 40)
    add_product_button = pygame.Rect(10, 550, 180, 40)
    users_button = pygame.Rect(10, 500, 180, 40)
    dropdown_box = pygame.Rect(220, 230, 300, 220)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    active_name = False
    active_price = False
    active_category = False
    text_name = ''
    text_price = ''
    delete = font.render("x", True, pygame.Color('black'))
    running = True

    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if login_mode:  # Pokud je aktivní přihlašovací režim
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if login_box_user.collidepoint(event.pos):
                        active_user = True
                        active_pass = False
                    elif login_box_pass.collidepoint(event.pos):
                        active_pass = True
                        active_user = False
                    elif login_button.collidepoint(event.pos):
                        if check_login(user_text, pass_text):  # Ověříme přihlašovací údaje
                            login_mode = False  # Přepneme na hlavní aplikaci
                        else:
                            login_error = True  # Chyba přihlášení

                if event.type == pygame.KEYDOWN:
                    if active_user:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            user_text += event.unicode
                    elif active_pass:
                        if event.key == pygame.K_BACKSPACE:
                            pass_text = pass_text[:-1]
                        else:
                            pass_text += event.unicode

            else:  # Zbytek aplikace (kategorie, produkty)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] < 200:
                        if add_product_button.collidepoint(event.pos):
                            view_mode = "input"
                        elif users_button.collidepoint(event.pos):
                            view_mode = "users"
                        else:
                            for i, category in enumerate(categories):
                                if event.pos[0] < 200:
                                    for i, category in enumerate(categories):
                                        category_rect = pygame.Rect(10, 10 + i * 40, 180, 30)
                                        if category_rect.collidepoint(event.pos):
                                            selected_category = category[0]  # Uložení ID kategorie (NE index!)
                                            products = get_products_by_category(selected_category)
                                            view_mode = "category_view"
                    elif view_mode == "category_view" and event.pos[0] < 200 and 10 <= event.pos[1] <= 40:
                        view_mode = "input"
                    elif view_mode == "input":
                        if input_box_name.collidepoint(event.pos):
                            active_name = True
                            active_price = False
                            active_category = False
                        elif input_box_price.collidepoint(event.pos):
                            active_price = True
                            active_name = False
                            active_category = False
                        elif category_box.collidepoint(event.pos):
                            dropdown_open = not dropdown_open
                        elif dropdown_open:
                            for i, category in enumerate(categories):
                                option_rect = pygame.Rect(220, 220 + (i + 1) * 35, 300, 32)
                                if option_rect.collidepoint(event.pos):
                                    selected_category = i
                                    dropdown_open = False
                        elif button_box.collidepoint(event.pos):
                            try:
                                insert_product(text_name, float(text_price), categories[selected_category][0])
                                text_name = ''
                                text_price = ''
                            except ValueError:
                                pass
                if event.type == pygame.KEYDOWN:
                    if active_name:
                        if event.key == pygame.K_BACKSPACE:
                            text_name = text_name[:-1]
                        else:
                            text_name += event.unicode
                    elif active_price:
                        if event.key == pygame.K_BACKSPACE:
                            text_price = text_price[:-1]
                        elif event.unicode.isdigit() or event.unicode == '.':
                            text_price += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if users_button.collidepoint(event.pos):
                        view_mode = "users"
                        users = get_users()


        if login_mode:
            # Přihlašovací obrazovka
            screen.fill((50, 50, 50))  # Pozadí
            user_label = font.render("Uživatel:", True, pygame.Color('white'))
            pass_label = font.render("Heslo:", True, pygame.Color('white'))
            screen.blit(user_label, (200, 205))
            screen.blit(pass_label, (200, 265))

            pygame.draw.rect(screen, color_active if active_user else color_inactive, login_box_user, 2)
            pygame.draw.rect(screen, color_active if active_pass else color_inactive, login_box_pass, 2)
            pygame.draw.rect(screen, pygame.Color('green'), login_button)

            user_surface = font.render(user_text, True, pygame.Color('white'))
            pass_surface = font.render('*' * len(pass_text), True, pygame.Color('white'))
            screen.blit(user_surface, (login_box_user.x + 5, login_box_user.y + 5))
            screen.blit(pass_surface, (login_box_pass.x + 5, login_box_pass.y + 5))

            login_text = font.render("Přihlásit", True, pygame.Color('white'))
            screen.blit(login_text, (login_button.x + 10, login_button.y + 10))

            if login_error:
                error_text = font.render("Neplatné přihlášení!", True, pygame.Color('red'))
                screen.blit(error_text, (300, 380))
        else:
            # Zbytek aplikace (vykreslení kategorií, produktů)
            pygame.draw.rect(screen, pygame.Color('black'), (0, 0, 200, 600))
            for i, category in enumerate(categories):
                category_text = font.render(category[1], True, pygame.Color('white'))
                screen.blit(category_text, (10, 10 + i * 40))
            pygame.draw.rect(screen, pygame.Color('blue'), add_product_button)
            add_product_text = font.render("Přidat produkt", True, pygame.Color('white'))
            screen.blit(add_product_text, (20, 560))
            pygame.draw.rect(screen, pygame.Color('blue'), users_button)
            users_button_text = font.render("Body", True, pygame.Color('white'))
            screen.blit(users_button_text, (20, 510))
            
            if view_mode == "input":
                name_label = font.render("Název produktu:", True, pygame.Color('white'))
                price_label = font.render("Cena produktu:", True, pygame.Color('white'))
                category_label = font.render("Kategorie:", True, pygame.Color('white'))
                screen.blit(name_label, (220, 70))
                screen.blit(price_label, (220, 135))
                screen.blit(category_label, (220, 200))
                
                pygame.draw.rect(screen, color_active if active_name else color_inactive, input_box_name, 2)
                pygame.draw.rect(screen, color_active if active_price else color_inactive, input_box_price, 2)
                pygame.draw.rect(screen, color_active if active_category else color_inactive, category_box, 2)
                pygame.draw.rect(screen, pygame.Color('green'), button_box)
                
                txt_surface_name = font.render(text_name, True, pygame.Color('white'))
                txt_surface_price = font.render(text_price, True, pygame.Color('white'))
                selected_category_text = font.render(categories[selected_category][1], True, pygame.Color('white'))
                screen.blit(txt_surface_name, (input_box_name.x+5, input_box_name.y+5))
                screen.blit(txt_surface_price, (input_box_price.x+5, input_box_price.y+5))
                screen.blit(selected_category_text, (category_box.x+5, category_box.y+5))

                if dropdown_open:
                    pygame.draw.rect(screen, pygame.Color('gray'), dropdown_box)
                    for i, category in enumerate(categories):
                        option_rect = pygame.Rect(220, 220 + (i + 1) * 35, 300, 32)
                        pygame.draw.rect(screen, pygame.Color('lightgray'), option_rect)
                        category_text = font.render(category[1], True, pygame.Color('black'))
                        screen.blit(category_text, (option_rect.x + 5, option_rect.y + 5))
                
                button_text = font.render("Přidat", True, pygame.Color('white'))
                screen.blit(button_text, (button_box.x+20, button_box.y+10))

            if view_mode == "category_view":
                title = font2.render(f"Produkty v kategorii: {next(c[1] for c in categories if c[0] == selected_category)}", True, pygame.Color('white'))
                screen.blit(title, (220, 40))

                y_offset = 120
                delete_buttons = []  # Seznam pro uložení tlačítek
                for product in products:
                    product_text = font.render(f"{product[0]} - {product[1]} Kč", True, pygame.Color('white'))
                    screen.blit(product_text, (260, y_offset))

                    delete_button = pygame.Rect(220, y_offset, 25, 25)
                    pygame.draw.rect(screen, pygame.Color('red'), delete_button)
                    screen.blit(delete, (delete_button.x + 5, delete_button.y + 2))

                    delete_buttons.append((delete_button, product[0]))  # Uložíme tlačítko a název produktu
                    y_offset += 40
                    
            if event.type == pygame.MOUSEBUTTONDOWN and view_mode == "category_view":
                for button, product_name in delete_buttons:
                    if button.collidepoint(event.pos):
                        delete_product(product_name)  # SMAŽEME PRODUKT
                        products = get_products_by_category(selected_category)  # AKTUALIZUJEME SEZNAM

            if view_mode == "users":
                y_offset = 20
                user_buttons = []
                for user in users:
                    username, points = user
                    user_text = font.render(f"{username}: {points} bodů", True, pygame.Color('white'))
                    screen.blit(user_text, (220, y_offset))

                    plus_button = pygame.Rect(400, y_offset, 30, 30)
                    minus_button = pygame.Rect(440, y_offset, 30, 30)
                    pygame.draw.rect(screen, pygame.Color('green'), plus_button)
                    pygame.draw.rect(screen, pygame.Color('red'), minus_button)

                    screen.blit(font.render("+", True, pygame.Color('white')), (plus_button.x + 8, plus_button.y + 3))
                    screen.blit(font.render("-", True, pygame.Color('white')), (minus_button.x + 10, minus_button.y + 3))

                    user_buttons.append((username, plus_button, minus_button))
                    y_offset += 40

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for username, plus_btn, minus_btn in user_buttons:
                        if plus_btn.collidepoint(event.pos):
                            update_user_points(username, 1)
                            users = get_users()  # Aktualizace dat
                        if minus_btn.collidepoint(event.pos):
                            update_user_points(username, -1)
                            users = get_users()  # Aktualizace dat

        pygame.display.flip()
        clock.tick(30)


    pygame.quit()

if __name__ == "__main__":
    main()

import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self) -> str:
        return f"{self.rank['rank']} of {self.suit}"

class Deck:
    def __init__(self): 
        self.cards = []
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
            {"rank": "A", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "J", "value": 10},
            {"rank": "Q", "value": 10},
            {"rank": "K", "value": 10}
        ]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []
        for x in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt 

class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "A":
                has_ace = True

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_cards=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand: ''')

        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack():
                print("Hidden")
            else:
                print(card)
        
        if not self.dealer:
            print("Value:", self.get_value())
        print() 

class Game:
    def play(self):
        game_number = 0
        games_to_play = 0

        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except:
                print("You must enter a number.")
        
        while game_number < games_to_play:
            game_number += 1 

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            choice = ""

            while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                choice = input("Please choose 'Hit' or 'Stand': ").lower()
                print()
                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please enter 'Hit' or 'Stand' (or H/S): ").lower()
                    print()
                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_cards=True)

            if self.check_winner(player_hand, dealer_hand):
                continue

            print("Final Results:")
            print("Your hand:", player_hand_value)
            print("Dealer's hand:", dealer_hand_value)

            self.check_winner(player_hand, dealer_hand, True)

        print("\nThanks for playing!")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You busted. Dealer wins! 😭")
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer busted. You win! 🏆")
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both players have a blackjack. It's a tie! 🤝")
                return True
            elif player_hand.is_blackjack():
                print("You have a blackjack. You win! 🏆")
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has a blackjack. Dealer wins! 😭")
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("You win! 🏆")
            elif player_hand.get_value() == dealer_hand.get_value():
                print("Tie! 🤝")
            else:
                print("Dealer wins! 😭")
            return True
        return False

# g = Game()
# g.play()

import tkinter as tk
from tkinter import messagebox

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        master.title("Blackjack")
        self.deck = None
        self.player_hand = None
        self.dealer_hand = None
        self.game_over = False

        # Layout
        self.dealer_label = tk.Label(master, text="Dealer's Hand:")
        self.dealer_label.pack()
        # Dealer hand canvas
        self.dealer_canvas = tk.Canvas(master, width=400, height=120, bg='green', highlightthickness=0)
        self.dealer_canvas.pack(pady=(0,5))
        self.dealer_value = tk.Label(master, text="")
        self.dealer_value.pack()

        self.player_label = tk.Label(master, text="Your Hand:")
        self.player_label.pack()
        self.player_canvas = tk.Canvas(master, width=400, height=120, bg='green', highlightthickness=0)
        self.player_canvas.pack(pady=(0,5))
        self.player_value = tk.Label(master, text="")
        self.player_value.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)
        self.hit_button = tk.Button(self.button_frame, text="Hit", width=10, command=self.hit)
        self.hit_button.grid(row=0, column=0, padx=5)
        self.stand_button = tk.Button(self.button_frame, text="Stand", width=10, command=self.stand)
        self.stand_button.grid(row=0, column=1, padx=5)
        self.new_game_button = tk.Button(self.button_frame, text="New Game", width=10, command=self.new_game)
        self.new_game_button.grid(row=0, column=2, padx=5)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack(pady=5)

        self.new_game()

    def new_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand(dealer=True)
        self.game_over = False
        # Deal initial cards
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal(1))
            self.dealer_hand.add_card(self.deck.deal(1))
        self.update_display(show_all_dealer_cards=False)
        self.status_label.config(text="Game started. Your move!")
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

        # Check for blackjack
        if self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
            self.end_game()

    def update_display(self, show_all_dealer_cards):
        # Helper for drawing cards
        def draw_hand(canvas, hand, hide_first_card=False):
            canvas.delete("all")
            card_width, card_height = 60, 90
            spacing = 20
            x0 = 10
            for idx, card in enumerate(hand.cards):
                x = x0 + idx * (card_width + spacing)
                y = 10
                if idx == 0 and hide_first_card and not hand.is_blackjack():
                    # Draw back of card
                    canvas.create_rectangle(x, y, x+card_width, y+card_height, fill="#224488", outline="white", width=2)
                    canvas.create_text(x+card_width/2, y+card_height/2, text="?", fill="white", font=("Arial", 28, "bold"))
                else:
                    suit = card.suit
                    rank = card.rank['rank']
                    suit_unicode = {"spades": "\u2660", "clubs": "\u2663", "hearts": "\u2665", "diamonds": "\u2666"}
                    suit_colors = {"spades": "black", "clubs": "black", "hearts": "red", "diamonds": "red"}
                    unicode_suit = suit_unicode.get(suit, "?")
                    color = suit_colors[suit]
                    canvas.create_rectangle(x, y, x+card_width, y+card_height, fill="white", outline="black", width=2)
                    canvas.create_text(x+card_width/2, y+card_height/2-15, text=rank, fill=color, font=("Arial", 20, "bold"))
                    canvas.create_text(x+card_width/2, y+card_height/2+15, text=unicode_suit, fill=color, font=("Arial", 28))
        # Draw dealer
        draw_hand(self.dealer_canvas, self.dealer_hand, hide_first_card=not show_all_dealer_cards)
        self.dealer_value.config(text=("Value: ?" if not show_all_dealer_cards else f"Value: {self.dealer_hand.get_value()}"))
        # Draw player
        draw_hand(self.player_canvas, self.player_hand, hide_first_card=False)
        self.player_value.config(text=f"Value: {self.player_hand.get_value()}")

    def hit(self):
        if self.game_over:
            return
        self.player_hand.add_card(self.deck.deal(1))
        self.update_display(show_all_dealer_cards=False)
        if self.player_hand.get_value() > 21:
            self.end_game()

    def stand(self):
        if self.game_over:
            return
        # Dealer's turn
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal(1))
        self.end_game()

    def end_game(self):
        self.game_over = True
        self.update_display(show_all_dealer_cards=True)
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        msg = ""
        if self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
            msg = "Both players have a blackjack. It's a tie! 🤝"
        elif self.player_hand.is_blackjack():
            msg = "You have a blackjack. You win! 🏆"
        elif self.dealer_hand.is_blackjack():
            msg = "Dealer has a blackjack. Dealer wins! 😭"
        elif player_value > 21:
            msg = "You busted. Dealer wins! 😭"
        elif dealer_value > 21:
            msg = "Dealer busted. You win! 🏆"
        elif player_value > dealer_value:
            msg = "You win! 🏆"
        elif player_value == dealer_value:
            msg = "Tie! 🤝"
        else:
            msg = "Dealer wins! 😭"
        self.status_label.config(text=msg)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        messagebox.showinfo("Game Over", msg)

if __name__ == "__main__":
    root = tk.Tk()
    gui = BlackjackGUI(root)
    root.mainloop()
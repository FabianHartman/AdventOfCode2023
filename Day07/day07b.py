class Hand:
    def __init__(self,cards, bet):
        self.bet = int(bet)
        self.cards = cards

    @staticmethod
    def parseInputString(inputString):
        return Hand(inputString.split(" ")[0],inputString.split(" ")[1])


    def getCardCounts(self):
        card_counts = {}
        for card in self.cards:
            if card in card_counts:
                card_counts[card]+=1
            else:
                card_counts[card]=1
        return card_counts

    def hasNOfAKind(self,n):
        card_counts = self.getCardCounts()
        amount_of_jokers = card_counts.get('J', 0)
        if amount_of_jokers == n: return True
        for key in card_counts:
            if key != "J":
                if card_counts[key] + amount_of_jokers == n:
                    return True
            else:
                if card_counts[key] == n:
                    return True
        return False

    def hasFullHouse(self):
        amount_of_types = 0
        total = 0
        card_counts = self.getCardCounts()
        amount_of_jokers = card_counts.get('J', 0)
        card_counts.pop("J",None)
        for key in card_counts:
            amount_of_types+=1
            total+= card_counts[key]
            if amount_of_types == 2:
                if total + amount_of_jokers == 5:
                    return True
                return False

    def getAmountOfPairs(self):
        card_counts = self.getCardCounts()
        amount_of_pairs = 0
        amount_of_jokers = card_counts.get('J', 0)
        card_counts.pop("J",None)
        for key in card_counts:
            if card_counts[key]>=2:
                amount_of_pairs+=1
                continue
            if card_counts[key]+amount_of_jokers>=2:
                amount_of_pairs+=1
                amount_of_jokers-=(2-card_counts[key])
                continue
        return amount_of_pairs

    def hasAmountOfPairs(self,amount):
        return self.getAmountOfPairs() == amount

    def getType(self):
        if self.hasNOfAKind(5): return 7
        if self.hasNOfAKind(4): return 6
        if self.hasFullHouse(): return 5
        if self.hasNOfAKind(3): return 4
        if self.hasAmountOfPairs(2): return 3
        if self. hasAmountOfPairs(1): return 2
        return 1

    def __str__(self):
        return f"{self.cards} {self.bet}"

class Game:
    def __init__(self,hands):
        self.hands = hands

    @staticmethod
    def parseInputStrings(inputStrings):
        hands = []
        for hand_input in inputStrings:
            hands.append(Hand.parseInputString(hand_input))
        return hands

    def getHandsSplitByType(self):
        hands_split_by_type = {}
        for hand in self.hands:
            hand_type = hand.getType()
            if hand_type in hands_split_by_type:
                hands_split_by_type[hand_type].append(hand)
            else:
                hands_split_by_type[hand_type] = [hand]
        return hands_split_by_type

    @staticmethod
    def insertIntoOrderedHandList(hand_list, hand):
        order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2','J']
        if len(hand_list) == 0:
            return [hand]
        for hand_in_list_i in range(len(hand_list)):
            hand_in_list = hand_list[hand_in_list_i]
            for char_i in range(len(hand.cards)):
                if order.index(hand.cards[char_i]) > order.index(hand_in_list.cards[char_i]):
                    hand_list.insert(hand_in_list_i, hand)
                    return hand_list
                elif order.index(hand.cards[char_i]) < order.index(hand_in_list.cards[char_i]):
                    break
        hand_list.append(hand)
        return hand_list

    def getHandOrder(self):
        ordered_hands = []
        hands_split_by_type = self.getHandsSplitByType()
        for hands_in_type in sorted(hands_split_by_type):
            ordered_hands_in_type = []
            for hand_in_type in hands_split_by_type[hands_in_type]:
                ordered_hands_in_type = Game.insertIntoOrderedHandList(ordered_hands_in_type,hand_in_type)
            ordered_hands += ordered_hands_in_type
        return ordered_hands

    def getTotalWinnings(self):
        total_winings = 0
        ordered_hands = self.getHandOrder()
        for hand_i in range(0,len(ordered_hands)):
            total_winings += (hand_i+1) * ordered_hands[hand_i].bet
        return total_winings






with open('./input.txt', 'r') as file:
    hands = Game.parseInputStrings(file.read().splitlines())
    game = Game(hands)
    print(game.getTotalWinnings())
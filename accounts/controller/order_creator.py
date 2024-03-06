from accounts.models import BaseUser, BaseOrder
from django.contrib.contenttypes.models import ContentType
from accounts.controller.utils import get_game
from accounts.models import PromoCode

def create_order(invoice, payer_id, customer, status='New',name = None):
    try :
        invoice_values = invoice.split('-')
        game_id = int(invoice_values[1])
        type = str(invoice_values[2])
        booster_id = int(invoice_values[12])
        extend_order_id = int(invoice_values[13])
        price = float(invoice_values[15])
        server = str(invoice_values[14]) ########### TODO make this int and go to invoice and make int
        if type == 'D' or type == 'A':
            current_rank =  int(invoice_values[3])
            current_division = int(invoice_values[4])
            current_marks = int(invoice_values[5])
            desired_rank = int(invoice_values[6])
            desired_division = int(invoice_values[7])
        elif type == 'P':
            last_rank = int(invoice_values[3])
            number_of_match = int(invoice_values[4])
        elif type == 'S':
            current_rank = int(invoice_values[3])
            number_of_wins = int(invoice_values[4])
        elif type == 'T':
            current_league = int(invoice_values[3])

        duo_boosting = bool(int(invoice_values[8]))
        select_booster = bool(int(invoice_values[9]))
        turbo_boost = bool(int(invoice_values[10]))
        streaming = bool(int(invoice_values[11]))

        select_champion = bool(int(invoice_values[16]))
        promo_code = str(invoice_values[17])
        role = int(invoice_values[18])
        ranked_type = int(invoice_values[19])
        

        
        
        
        try:
            promo_obj = PromoCode.objects.get(name = promo_code)
            promo_code_amount = promo_obj.discount_amount
        except:
            promo_code_amount = 0
        try:
            booster = BaseUser.objects.get(id=booster_id, is_booster =True)
        except BaseUser.DoesNotExist:
            booster = None

        Game = get_game(game_id, type)        
        try:
            if status != 'Continue':
                extend_order = BaseOrder.objects.get(id=extend_order_id)
                extend_order.is_done = True
                extend_order.is_extended = True
                extend_order.money_owed = 0
                extend_order.status = 'Extend'
                extend_order.save()
                status = 'Extend'
                
                extend_order_money_owed = extend_order.money_owed
                extend_order_price = extend_order.price
                order_name = extend_order.name
                extend_order_booster = extend_order.booster
                extend_order_customer = extend_order.customer
                extend_order_customer_gamename = extend_order.customer_gamename
                extend_order_customer_password = extend_order.customer_password
                extend_order_server = extend_order.customer_server
                extend_order_data_correct = extend_order.data_correct
                extend_order_promo_code = extend_order.promo_code

                extend_order_game = Game.objects.get(order = extend_order)
                extend_order_game_reached_rank = extend_order_game.reached_rank
                extend_order_game_reached_division = extend_order_game.reached_division
                extend_order_game_reached_marks = extend_order_game.reached_marks  

                if game_id == 12 :
                    extend_order_role = extend_order_game.role
                     

        except BaseOrder.DoesNotExist:
            extend_order = None

        if status == 'New' or status == 'Continue':
            baseOrder = BaseOrder.objects.create(invoice=invoice, booster=booster, payer_id=payer_id, customer=customer,status=status, price=price, duo_boosting=duo_boosting,select_booster=select_booster,turbo_boost=turbo_boost,streaming=streaming, name=name, customer_server=server,promo_code= promo_code_amount)
            # Here I Make This Condition Because it Make Error in Placement
            if type == 'D':
                default_fields = {
                    'order': baseOrder,
                    'current_rank_id': current_rank,
                    'current_division': current_division,
                    'current_marks': current_marks,
                    'desired_rank_id': desired_rank,
                    'desired_division': desired_division,
                    'reached_rank_id': current_rank,
                    'reached_division': current_division,
                    'reached_marks': current_marks,
                }
            # Wildrift Without Placement 
            if game_id == 1:
                order = Game.objects.create(**default_fields, booster_champions=select_champion)
            # Valorant - Division
            elif game_id == 2 and type == 'D':
                order = Game.objects.create(**default_fields, choose_agents=select_champion)
            # Valorant - Placement
            elif game_id == 2 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_agents=select_champion)
            # Pubg Without Placement 
            elif game_id == 3:
                order = Game.objects.create(**default_fields, choose_agents=select_champion)
            # LOL - Division
            elif game_id == 4 and type == 'D':
                order = Game.objects.create(**default_fields, choose_champions=select_champion)
            # LOL - Placement
            elif game_id == 4 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_champions=select_champion)
            # TFT - Division
            elif game_id == 5 and type == 'D':
                order = Game.objects.create(**default_fields)
            # TFT - Placement
            elif game_id == 5 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match)
            # WoW - Arena
            elif game_id == 6 and type == 'A':
                order = Game.objects.create(**extend_fields, choose_agents=select_champion)
            # HEARTHSTONE
            elif game_id == 7 and type == 'D':
                order = Game.objects.create(**default_fields, choose_legends=select_champion)
            # Mobile Legends - Division
            elif game_id == 8 and type == 'D':
                order = Game.objects.create(**default_fields, choose_champions=select_champion)
            # Mobile Legends - Placement
            elif game_id == 8 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_champions=select_champion)
            # Rocket League - Division
            elif game_id == 9 and type == 'D':
                order = Game.objects.create(**default_fields, ranked_type=ranked_type)
            # Rocket League - Placement
            elif game_id == 9 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=last_rank,number_of_match=number_of_match)
            # Rocket League - Seasonal
            elif game_id == 9 and type == 'S':
                order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,number_of_wins=number_of_wins)
            # Rocket League - Tournament
            elif game_id == 9 and type == 'T':
                order = Game.objects.create(order=baseOrder,current_league_id=current_league)
            # TODO sara kamal Doat2          #########
            if game_id == 10:
                pass
            #TODO sarah mohamed Honer Of King #########
            if game_id == 11:
                order = Game.objects.create(**default_fields,select_champion=select_champion)
            # Overwatch Division 
            if game_id == 12 and type == 'D':
                order = Game.objects.create(**default_fields, role=role)
            # csgo2
            if game_id == 13:
                pass

        elif status == 'Extend':
            print(f"order extended from:  {order_name}")
            baseOrder = BaseOrder.objects.create(invoice=invoice, booster=extend_order_booster,duo_boosting=duo_boosting, select_booster=select_booster, turbo_boost=turbo_boost,streaming=streaming, customer=extend_order_customer,payer_id=payer_id, customer_gamename=extend_order_customer_gamename, customer_password=extend_order_customer_password, customer_server=extend_order_server,name = order_name, money_owed =extend_order_money_owed, price = price + extend_order_price, data_correct = extend_order_data_correct,promo_code=extend_order_promo_code, status = "Extend")
            extend_fields = {
                'order': baseOrder,
                'current_rank_id': current_rank,
                'current_division': current_division,
                'current_marks': current_marks,
                'desired_rank_id': desired_rank,
                'desired_division': desired_division,
                'reached_rank': extend_order_game_reached_rank,
                'reached_division': extend_order_game_reached_division,
                'reached_marks': extend_order_game_reached_marks,
            }

            # Wildrift Without Placement 
            if game_id == 1:
                order = Game.objects.create(**extend_fields, booster_champions=select_champion)
            # Valorant - Division
            elif game_id == 2 and type == 'D':
                order = Game.objects.create(**extend_fields, choose_agents=select_champion)
            # Valorant - Placement
            elif game_id == 2 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_agents=select_champion)       
            # Pubg Without Placement 
            elif game_id == 3:
                order = Game.objects.create(**extend_fields, choose_agents=select_champion)
            # LOL - Division
            elif game_id == 4 and type == 'D':
                order = Game.objects.create(**extend_fields, choose_champions=select_champion)
            # LOL - Placement
            elif game_id == 4 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_champions=select_champion)
            # TFT - Division
            elif game_id == 5 and type == 'D':
                order = Game.objects.create(**extend_fields, speed_up_boost=turbo_boost)
            # TFT - Placement
            elif game_id == 5 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match)
            # WoW
            elif game_id == 6 and type == 'A':
                # TODO not completed yet
                order = Game.objects.create(**extend_fields)
            # HEARTHSTONE
            elif game_id == 7:
                order = Game.objects.create(**extend_fields, choose_legends=select_champion)
            # Mobile Legends
            elif game_id == 8 and type == 'D': 
                order = Game.objects.create(**extend_fields, choose_champions=select_champion)

            elif game_id == 8 and type == 'P': 
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_champions=select_champion)

            # Rocket League - Division
            elif game_id == 9 and type == 'D':
                order = Game.objects.create(**extend_fields, ranked_type=ranked_type)
            # Rocket League - Placement
            elif game_id == 9 and type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=last_rank,number_of_match=number_of_match)
            # Rocket League - Seasonal
            elif game_id == 9 and type == 'S':
                order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,number_of_wins=number_of_wins)
            # Rocket League - Tournament
            elif game_id == 9 and type == 'T':
                order = Game.objects.create(order=baseOrder,current_league_id=current_league)
            # TODO sara kamal Doat2      TODO       ########
            if game_id == 10:
                pass
            #TODO sarah mohamed Honer Of King      TODO      #########
            if game_id == 11:
                order = Game.objects.create(**extend_fields)
            # Overwatch Division 
            if game_id == 12 and type == 'D':
                order = Game.objects.create(**extend_fields, role= extend_order_role)
            # csgo2
            if game_id == 13:
                pass
        content_type = ContentType.objects.get_for_model(order)
        baseOrder.content_type = content_type
        baseOrder.object_id = order.pk
        order.save_with_processing()
        baseOrder.customer_wallet()
        return order
    
    except Exception as e:
        print(f"Error creating order: {e}")
        return None
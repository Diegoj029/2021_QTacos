import pygame as pg
import os
"""
///////////////////////////////////////////////////////////
    IMPORT RESOURCES
///////////////////////////////////////////////////////////
"""
game_folder = os.path.dirname(os.path.abspath(__file__))

game_bg = pg.image.load(os.path.join(game_folder,'resources/backgrounds/game.png'))
main_menu_bg = pg.image.load(os.path.join(game_folder,'resources/backgrounds/main_menu.png'))
#credits_bg = pg.image.load(os.path.join(game_folder,'resources/backgrounds/credits.png'))

plate = pg.image.load(os.path.join(game_folder,'resources/images/plate.png'))

tortilla = pg.image.load(os.path.join(game_folder,'resources/images/tortilla.png'))

deshebrada = pg.image.load(os.path.join(game_folder,'resources/images/deshebrada.png'))
trompo = pg.image.load(os.path.join(game_folder,'resources/images/trompo.png'))
pastor = pg.image.load(os.path.join(game_folder,'resources/images/pastor.png'))
cilantro = pg.image.load(os.path.join(game_folder,'resources/images/cilantro.png'))
cebolla = pg.image.load(os.path.join(game_folder,'resources/images/cebolla.png'))
chicken = pg.image.load(os.path.join(game_folder,'resources/images/chicken.png'))

tortilla_glow = pg.image.load(os.path.join(game_folder,'resources/images/tortilla_glow.png'))
deshebrada_glow = pg.image.load(os.path.join(game_folder,'resources/images/deshebrada_glow.png'))
trompo_glow = pg.image.load(os.path.join(game_folder,'resources/images/trompo_glow.png'))
cilantro_glow = pg.image.load(os.path.join(game_folder,'resources/images/cilantro_glow.png'))
cebolla_glow = pg.image.load(os.path.join(game_folder,'resources/images/cebolla_glow.png'))
chicken_glow = pg.image.load(os.path.join(game_folder,'resources/images/chicken_glow.png'))

paper = pg.image.load(os.path.join(game_folder,'resources/images/paper.png'))
paper_glow = pg.image.load(os.path.join(game_folder,'resources/images/paper_glow.png'))
canasta = pg.image.load(os.path.join(game_folder,'resources/images/canasta.png'))
canasta_glow = pg.image.load(os.path.join(game_folder,'resources/images/canasta_glow.png'))
no_glow = pg.image.load(os.path.join(game_folder,'resources/images/no_glow.png'))

play = pg.image.load(os.path.join(game_folder,'resources/buttons/play.png'))
play_glow = pg.image.load(os.path.join(game_folder,'resources/buttons/play_glow.png'))
leaderboard = pg.image.load(os.path.join(game_folder,'resources/buttons/leaderboard.png'))
leaderboard_glow = pg.image.load(os.path.join(game_folder,'resources/buttons/leaderboard_glow.png'))
howtoplay = pg.image.load(os.path.join(game_folder,'resources/buttons/howtoplay.png'))
howtoplay_glow = pg.image.load(os.path.join(game_folder,'resources/buttons/howtoplay_glow.png'))
options = pg.image.load(os.path.join(game_folder,'resources/buttons/options.png'))
options_glow = pg.image.load(os.path.join(game_folder,'resources/buttons/options_glow.png'))
cred = pg.image.load(os.path.join(game_folder,'resources/buttons/credits.png'))
cred_glow = pg.image.load(os.path.join(game_folder,'resources/buttons/credits_glow.png'))
back = pg.image.load(os.path.join(game_folder,'resources/buttons/back.png'))
back_glow = pg.image.load(os.path.join(game_folder,'resources/buttons/back_glow.png'))

songs = [os.path.join(game_folder,'resources/music/acosta.ogg'), os.path.join(game_folder,'resources/music/ramito.ogg')]
leaderboard_txt = os.path.join(game_folder,'resources/docs/leaderboard.csv')
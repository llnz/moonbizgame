
import random
import datetime

from launch.models import Launch, LaunchConfig

def start_game(enterprise):
    '''Create the initial universe for the enterprise to play with'''
    
    universe = enterprise.universe
    
    for _i in range(random.randint(5, 10)):
        create_launch(universe)
    
    
def create_launch(universe):
    '''Create a random launch'''
    
    launch = Launch(universe=universe)
    launch.when_igt = universe.current_time + datetime.timedelta(days=1 + random.randint(0, 15))
    
    company_num = random.randint(0, 10)
    
    if company_num in (0, 1, 2):
        launch.company = 'SpaceX'
        
        if random.randint(0, 10) < 9:
            launch.product = 'Falcon 9'
            launch.save()
            
            for pos in range(1, 4): 
                config = LaunchConfig(launch=launch, config_group=1, config_position=pos)
                config.max_mass = 190
                config.price = 19000000
                config.destination = 'Moon Surface'
                config.save()
            
            for pos in range(1, 4): 
                config = LaunchConfig(launch=launch, config_group=2, config_position=pos)
                config.max_mass = 580
                config.price = 18000000
                config.destination = 'Moon Orbit'
                config.save()
                
            config = LaunchConfig(launch=launch, config_group=3, config_position=1)
            config.max_mass = 1600
            config.price = 58000000
            config.destination = 'Moon Orbit'
            config.save()
            
            
        else:
            launch.product = 'Falcon Heavy'
            launch.save()
            
            for pos in range(1, 4): 
                config = LaunchConfig(launch=launch, config_group=1, config_position=pos)
                config.max_mass = 780
                config.price = 50000000
                config.destination = 'Moon Surface'
                config.save()
            
            for pos in range(1, 4): 
                config = LaunchConfig(launch=launch, config_group=2, config_position=pos)
                config.max_mass = 1290
                config.price = 42000000
                config.destination = 'Moon Orbit'
                config.save()
                
            config = LaunchConfig(launch=launch, config_group=3, config_position=1)
            config.max_mass = 5200
            config.price = 120000000
            config.destination = 'Moon Orbit'
            config.save()
            
    elif company_num in (3, 4, 5, 6, 7, 8):
        launch.company = 'United Launch Alliance'
        
        if company_num in (3, 4):
            launch.product = 'Atlas V'
            launch.save()
            
            config = LaunchConfig(launch=launch, config_group=1, config_position=1)
            config.max_mass = 180
            config.price = 240000000
            config.destination = 'Moon Surface'
            config.save()
            
            config = LaunchConfig(launch=launch, config_group=2, config_position=1)
            config.max_mass = 570
            config.price = 230000000
            config.destination = 'Moon Orbit'
            config.save()
            
        elif company_num in (5, 6):
            launch.product = 'Delta II'
            launch.save()
            
            config = LaunchConfig(launch=launch, config_group=1, config_position=1)
            config.max_mass = 210
            config.price = 240000000
            config.destination = 'Moon Surface'
            config.save()
            
            config = LaunchConfig(launch=launch, config_group=2, config_position=1)
            config.max_mass = 590
            config.price = 230000000
            config.destination = 'Moon Orbit'
            config.save()
            
        elif company_num == 7:
            launch.product = 'Delta IV'
            launch.save()
            
            config = LaunchConfig(launch=launch, config_group=1, config_position=1)
            config.max_mass = 360
            config.price = 240000000
            config.destination = 'Moon Surface'
            config.save()
            
            config = LaunchConfig(launch=launch, config_group=2, config_position=1)
            config.max_mass = 740
            config.price = 230000000
            config.destination = 'Moon Orbit'
            config.save()
            
        else:
            launch.product = 'Delta IV Heavy'
            launch.save()
            
            for pos in range(1, 4): 
                config = LaunchConfig(launch=launch, config_group=1, config_position=pos)
                config.max_mass = 810
                config.price = 64000000
                config.destination = 'Moon Surface'
                config.save()
            
            for pos in range(1, 4): 
                config = LaunchConfig(launch=launch, config_group=2, config_position=pos)
                config.max_mass = 1340
                config.price = 63000000
                config.destination = 'Moon Orbit'
                config.save()
                
            config = LaunchConfig(launch=launch, config_group=3, config_position=1)
            config.max_mass = 5400
            config.price = 182000000
            config.destination = 'Moon Orbit'
            config.save()
    
    else:
        launch.company = 'Orbital Sciences'
        launch.product = 'Minotaur V'
        launch.save()
        
        config = LaunchConfig(launch=launch, config_group=1, config_position=1)
        config.max_mass = 180
        config.price = 240000000
        config.destination = 'Moon Surface'
        config.save()
        
        config = LaunchConfig(launch=launch, config_group=2, config_position=1)
        config.max_mass = 570
        config.price = 230000000
        config.destination = 'Moon Orbit'
        config.save()
    
    
    

def end_turn(enterprise):
    '''End the turn/day
    
    Move everything on
    '''
    
    universe = enterprise.universe
    universe.current_time = universe.current_time + datetime.timedelta(days=1)
    universe.save()
    
    for _i in range(random.randint(1, 2)):
        create_launch(universe)
import os
import neat
import pickle

from classes import Game
from config import txt_config, number_of_generations

def model_exists() -> bool:
    return os.path.exists("./model/model.pkl")

def save_model(model) -> None:
    with open("./model/model.pkl", "wb") as file:
        pickle.dump(model, file)
        file.close()

def load_model():
    with open("./model/model.pkl", "rb") as file:
        model = pickle.load(file)
        file.close()

    return model

def main() -> None:
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        txt_config
    )

    # Generating a population based on the config file
    population = neat.Population(config)
    # Adding useful info in the console
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    model = population.run(Game().run, number_of_generations) 
    
    save_model(model)

main()
import logging
import os
from datetime import datetime

def setup_logging(game_name, model1_name, model2_name):
    # Create timestamped log directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join('logs', game_name, f"{timestamp}")
    os.makedirs(log_dir, exist_ok=True)

    # Setup main logger
    main_logger = logging.getLogger('main')
    main_logger.setLevel(logging.INFO)
    main_handler = logging.FileHandler(os.path.join(log_dir, 'main.log'))
    main_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    main_handler.setFormatter(main_formatter)
    main_logger.addHandler(main_handler)

    # Setup model1 logger
    model1_logger = logging.getLogger(f'model_{model1_name}_1')
    model1_logger.setLevel(logging.INFO)
    model1_handler = logging.FileHandler(os.path.join(log_dir, f'{model1_name}_1.log'))
    model1_formatter = logging.Formatter('--------------------------%(asctime)s--------------------------\n%(message)s')
    model1_handler.setFormatter(model1_formatter)
    model1_logger.addHandler(model1_handler)

    # Setup model2 logger
    model2_logger = logging.getLogger(f'model_{model2_name}_2')
    model2_logger.setLevel(logging.INFO)
    model2_handler = logging.FileHandler(os.path.join(log_dir, f'{model2_name}_2.log'))
    model2_formatter = logging.Formatter('--------------------------%(asctime)s--------------------------\n%(message)s')
    model2_handler.setFormatter(model2_formatter)
    model2_logger.addHandler(model2_handler)

    return main_logger, model1_logger, model2_logger
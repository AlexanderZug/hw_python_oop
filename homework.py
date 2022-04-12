from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MSG: ClassVar[str] = ('Тип тренировки: {}; '
                          'Длительность: {:.3f} ч.; '
                          'Дистанция: {:.3f} км; '
                          'Ср. скорость: {:.3f} км/ч; '
                          'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        """Вывод информации на экран."""
        items = asdict(self)
        return self.MSG.format(*items.values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Метод get_spent_calories '
                                  f'не был определен в классе '
                                  f'{type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        msg = InfoMessage(type(self).__name__, self.duration_h,
                          self.get_distance(),
                          self.get_mean_speed(),
                          self.get_spent_calories())
        return msg


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER_FIRST: int = 18
    CALORIES_MEAN_SPEED_MULTIPLIER_SECOND: int = 20

    def get_spent_calories(self) -> float:
        """Расчет калорий при беге."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER_FIRST
                 * self.get_mean_speed()
                 - self.CALORIES_MEAN_SPEED_MULTIPLIER_SECOND)
                * self.weight / self.M_IN_KM
                * (self.duration_h * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER_FIRST: float = 0.035
    CALORIES_MEAN_SPEED_MULTIPLIER_SECOND: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет калорий при ходьбе."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER_FIRST * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.CALORIES_MEAN_SPEED_MULTIPLIER_SECOND * self.weight)
                * (self.duration_h * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER_FIRST: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER_SECOND: float = 2.0

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action,
                         duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость при плавании."""
        return (self.length_pool_m * self.count_pool / self.M_IN_KM
                / self.duration_h)

    def get_spent_calories(self) -> float:
        """Расчет калорий при плавании."""
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_MULTIPLIER_FIRST)
                * self.CALORIES_MEAN_SPEED_MULTIPLIER_SECOND * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        training_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                    'RUN': Running,
                                                    'WLK': SportsWalking}
        return training_type.get(workout_type)(*data)
    except (ValueError, TypeError, AttributeError) as ex:
        print(f'Сегодня останешься без тренировки, прости, '
              f'но делать нечего - у нас ошибка: {ex}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('GGR', [88, 2, 0]),  # тест-ошибка
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

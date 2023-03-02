from dataclasses import asdict, dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о тренировке."""
        return (InfoMessage(self.__class__.__name__,
                self.duration, self.get_distance(),
                self.get_mean_speed(), self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
# Чтобы сократить код убрал функцию init
# По сути она повторяет то же что и в родительском классе
# Смысла в ней здесь нет тк я ничего в нее не перезаписываю :)

    def get_spent_calories(self) -> float:
        """Получить количество калорий во время бега"""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    CALORIES_WEIGHT_COEF: float = 0.035
    CALORIES_HEIGHT_COEF: float = 0.029
    KMH_TO_MS: float = 0.278
    CM_TO_M: int = 100
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество калорий во время ходьбы"""

        return ((self.CALORIES_WEIGHT_COEF * self.weight
                 + ((self.get_mean_speed() * self.KMH_TO_MS) ** 2
                    / (self.height / self.CM_TO_M))
                 * self.CALORIES_HEIGHT_COEF * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    LEN_STEP = 1.38
    SPEED_SHIFT: float = 1.1
    SPEED_MULTIPLIER: int = 2
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить ср. скорость пловца в км/ч"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество калорий во время плавания"""
        return ((self.get_mean_speed() + self.SPEED_SHIFT)
                * self.SPEED_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Считываем данные полученные от датчиков."""
    training_data: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in training_data:
        raise ValueError('Неизвестная тренировка')
    return training_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)

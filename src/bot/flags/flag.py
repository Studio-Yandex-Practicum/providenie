from core.logger import logger


class Flags:
    """Флаги:
    Режима редактирования данных,
    Режим первого старта,
    Режим невалидного ввода.
    """

    edit_mode_first_flag = False
    edit_mode_second_flag = False
    # first_start = False
    first_start = True
    bad_request = False
    first_start_menu = True
    first_start_volonteer = False

    def changing_edit_mode_first(self, edit_mode: bool):
        """Смена флага edit_mode_first_flag."""
        if isinstance(edit_mode, bool):
            Flags.edit_mode_first_flag = edit_mode
        else:
            msg = f"Неверный тип флага {edit_mode}!"
            logger.error(msg)

    def changing_edit_mode_second(self, edit_mode: bool):
        """Смена флага edit_mode_second_flag."""
        if isinstance(edit_mode, bool):
            Flags.edit_mode_second_flag = edit_mode
        else:
            msg = f"Неверный тип флага {edit_mode}!"
            logger.error(msg)

    def changing_first_start(self, first_start: bool):
        """Смена флага first_start."""
        if isinstance(first_start, bool):
            Flags.first_start = first_start
        else:
            msg = f"Неверный тип флага {first_start}!"
            logger.error(msg)

    def changing_bad_request(self, bad_request: bool):
        """Смена флага bad_request."""
        if isinstance(bad_request, bool):
            Flags.bad_request = bad_request
        else:
            msg = f"Неверный тип флага {bad_request}!"
            logger.error(msg)

    def changing_first_start_menu(self, first_start_menu: bool):
        """Смена флага first_start_menu."""
        if isinstance(first_start_menu, bool):
            Flags.first_start_menu = first_start_menu
        else:
            msg = f"Неверный тип флага {first_start_menu}!"
            logger.error(msg)

    def changing_first_start_volonteer(self, first_start_volonteer: bool):
        """Смена флага first_start_volonteer."""
        if isinstance(first_start_volonteer, bool):
            Flags.first_start_volonteer = first_start_volonteer
        else:
            msg = f"Неверный тип флага {first_start_volonteer}!"
            logger.error(msg)

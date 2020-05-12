import logging

from django.utils.datetime_safe import date
# from models import Pin_scores

logger = logging.getLogger(__name__)


def calculate_pins(ps_dict):
    """Calculates the pins based off of target size, distance, bow class and score"""
    # distance = int(ps_dict['distance'])
    # target = int(ps_dict['target'])
    # score = int(ps_dict['score'])
    #
    # star_achievement = 0
    # if ps_dict['category'] == 'joad_indoor':
    #     if ps_dict['bow'] == 'barebow':
    #         if distance == 9 and target == 60:
    #             if score >= 40:
    #                 star_achievement = 1
    #             if score >= 75:
    #                 star_achievement = 2
    #             if score >= 110:
    #                 star_achievement = 3
    #             if score >= 145:
    #                 star_achievement = 4
    #         elif distance == 18 and target == 60:
    #             if score >= 30:
    #                 star_achievement = 2
    #             if score >= 50:
    #                 star_achievement = 3
    #             if score >= 100:
    #                 star_achievement = 4
    #             if score >= 140:
    #                 star_achievement = 5
    #             if score >= 185:
    #                 star_achievement = 6
    #             if score >= 230:
    #                 star_achievement = 7
    #             if score >= 255:
    #                 star_achievement = 8
    #             if score >= 265:
    #                 star_achievement = 9
    #             if score >= 275:
    #                 star_achievement = 10
    #             if score >= 280:
    #                 star_achievement = 11
    #         elif distance == 18 and target == 40:
    #             if score >= 175:
    #                 star_achievement = 6
    #             if score >= 220:
    #                 star_achievement = 7
    #             if score >= 240:
    #                 star_achievement = 8
    #             if score >= 250:
    #                 star_achievement = 9
    #             if score >= 260:
    #                 star_achievement = 10
    #             if score >= 270:
    #                 star_achievement = 11
    #     elif ps_dict['bow'] == 'olympic':
    #         parameters = [
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 29, 'out': 0},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 30, 'out': 2},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 49, 'out': 2},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 50, 'out': 3},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 99, 'out': 3},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 100, 'out': 4},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 149, 'out': 4},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 150, 'out': 5},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 199, 'out': 5},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 200, 'out': 6},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 249, 'out': 6},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 250, 'out': 7},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 269, 'out': 7},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 270, 'out': 8},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 284, 'out': 8},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 285, 'out': 9},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 289, 'out': 9},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 290, 'out': 10},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 294, 'out': 10},
    #             {'category': 'joad_indoor', 'bow': 'olympic', 'distance': 18, 'target': 60, 'score': 295, 'out': 11},
    #         ]
    #         if distance == 9 and target == 60:
    #
    #             if score >= 50:
    #                 star_achievement = 1
    #             if score >= 100:
    #                 star_achievement = 2
    #             if score >= 150:
    #                 star_achievement = 3
    #             if score >= 200:
    #                 star_achievement = 4
    #
    #         elif distance == 18 and target == 60:
    #             if score >= 30:
    #                 star_achievement = 2
    #             if score >= 50:
    #                 star_achievement = 3
    #             if score >= 100:
    #                 star_achievement = 4
    #             if score >= 150:
    #                 star_achievement = 5
    #             if score >= 200:
    #                 star_achievement = 6
    #             if score >= 250:
    #                 star_achievement = 7
    #             if score >= 270:
    #                 star_achievement = 8
    #             if score >= 285:
    #                 star_achievement = 9
    #             if score >= 290:
    #                 star_achievement = 10
    #             if score >= 295:
    #                 star_achievement = 11
    #
    #         elif distance == 18 and target == 40:
    #             if score >= 190:
    #                 star_achievement = 6
    #             if score >= 240:
    #                 star_achievement = 7
    #             if score >= 260:
    #                 star_achievement = 8
    #             if score >= 280:
    #                 star_achievement = 9
    #             if score >= 285:
    #                 star_achievement = 10
    #             if score >= 290:
    #                 star_achievement = 11
    #     elif ps_dict['bow'] == 'compound':
    #         if distance == 9 and target == 40:
    #             if score >= 50:
    #                 star_achievement = 1
    #             if score >= 100:
    #                 star_achievement = 2
    #             if score >= 150:
    #                 star_achievement = 3
    #             if score >= 200:
    #                 star_achievement = 4
    #         elif distance == 18 and target == 40:
    #             if score >= 30:
    #                 star_achievement = 2
    #             if score >= 50:
    #                 star_achievement = 3
    #             if score >= 100:
    #                 star_achievement = 4
    #             if score >= 150:
    #                 star_achievement = 5
    #             if score >= 200:
    #                 star_achievement = 6
    #             if score >= 240:
    #                 star_achievement = 7
    #             if score >= 260:
    #                 star_achievement = 8
    #             if score >= 285:
    #                 star_achievement = 9
    #             if score >= 290:
    #                 star_achievement = 10
    #             if score >= 295:
    #                 star_achievement = 11
    # elif ps_dict['category'] == 'adult_indoor':
    #     if ps_dict['bow'] == 'barebow':
    #         if score >= 70:
    #             star_achievement = 1
    #         if score >= 100:
    #             star_achievement = 2
    #         if score >= 120:
    #             star_achievement = 3
    #         if score >= 150:
    #             star_achievement = 4
    #         if score >= 175:
    #             star_achievement = 5
    #         if score >= 200:
    #             star_achievement = 6
    #         if score >= 225:
    #             star_achievement = 7
    #         if score >= 240:
    #             star_achievement = 8
    #         if score >= 250:
    #             star_achievement = 9
    #         if score >= 260:
    #             star_achievement = 10
    #         if score >= 270:
    #             star_achievement = 11
    #     elif ps_dict['bow'] == 'olympic':
    #         if score >= 90: star_achievement = 1
    #         if score >= 140: star_achievement = 2
    #         if score >= 190: star_achievement = 3
    #         if score >= 210: star_achievement = 4
    #         if score >= 230: star_achievement = 5
    #         if score >= 250: star_achievement = 6
    #         if score >= 265: star_achievement = 7
    #         if score >= 270: star_achievement = 8
    #         if score >= 285: star_achievement = 9
    #         if score >= 290: star_achievement = 10
    #         if score >= 295: star_achievement = 11
    #     elif ps_dict['bow'] == 'compound':
    #         if score >= 125:
    #             star_achievement = 2  # TODO check this is it supposed to be 1?
    #         if score >= 150:
    #             star_achievement = 2
    #         if score >= 175:
    #             star_achievement = 3
    #         if score >= 200:
    #             star_achievement = 4
    #         if score >= 220:
    #             star_achievement = 5
    #         if score >= 240:
    #             star_achievement = 6
    #         if score >= 260:
    #             star_achievement = 7
    #         if score >= 270:
    #             star_achievement = 8
    #         if score >= 280:
    #             star_achievement = 9
    #         if score >= 285:
    #             star_achievement = 10
    #         if score >= 290:
    #             star_achievement = 11
    #
    # ps_dict['stars'] = star_achievement
    star_achievement = 0
    rows = Pin_scores.objects.filter(category=ps_dict['category'],
                              bow=ps_dict['bow'],
                              distance=ps_dict['distance'],
                              target=ps_dict['target'],
                              score__lte=ps_dict['score'])
    logging.debug(rows)
    return star_achievement


def joad_check_date(dob):
    d = date.today()
    logging.debug(d.year)
    d = d.replace(year=d.year - 21)
    logging.debug(dob)
    return dob > d

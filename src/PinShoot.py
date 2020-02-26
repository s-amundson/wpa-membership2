class PinShoot:
    def __init__(self, db):
        self.db = db
        self.ps_dict = {'first_name': '', 'last_name': '', 'club': '', 'category': '', 'bow': '',
                        'shoot_date': '', 'distance': '', 'target': '', 'star_achievement': '',
                        'wpa_membership_number': '', 'score': 0}
        if self.db is None:
            print(self.calculate_pins('joad_indoor', 'barebow', 60, 9, 120))

    def calculate_pins(self, category, bow, target, distance, score):
        print(f"target = {target} {type(target)}, distance = {distance} {type(distance)}")
        star_achievement = 0
        if category == 'joad_indoor':
            if bow == 'barebow':
                if distance == 9 and target == 60:
                    if score >= 40:
                        star_achievement = 1
                    if score >= 75:
                        star_achievement = 2
                    if score >= 110:
                        star_achievement = 3
                    if score >= 145:
                        star_achievement = 4
                elif distance == 18 and target == 60:
                    if score >= 30:
                        star_achievement = 2
                    if score >= 50:
                        star_achievement = 3
                    if score >= 100:
                        star_achievement = 4
                    if score >= 140:
                        star_achievement = 5
                    if score >= 185:
                        star_achievement = 6
                    if score >= 230:
                        star_achievement = 7
                    if score >= 255:
                        star_achievement = 8
                    if score >= 265:
                        star_achievement = 9
                    if score >= 275:
                        star_achievement = 10
                    if score >= 280:
                        star_achievement = 11
                elif distance == 18 and target == 40:
                    if score >= 175:
                        star_achievement = 6
                    if score >= 220:
                        star_achievement = 7
                    if score >= 240:
                        star_achievement = 8
                    if score >= 250:
                        star_achievement = 9
                    if score >= 260:
                        star_achievement = 10
                    if score >= 270:
                        star_achievement = 11
                # else:
                # form.errors.distance = "not distance and target combination"
            elif bow == 'olympic':
                if distance == 9 and target == 60:
                    if score >= 50:
                        star_achievement = 1
                    if score >= 100:
                        star_achievement = 2
                    if score >= 150:
                        star_achievement = 3
                    if score >= 200:
                        star_achievement = 4
                elif distance == 18 and target == 60:
                    if score >= 30:
                        star_achievement = 2
                    if score >= 50:
                        star_achievement = 3
                    if score >= 100:
                        star_achievement = 4
                    if score >= 150:
                        star_achievement = 5
                    if score >= 200:
                        star_achievement = 6
                    if score >= 250:
                        star_achievement = 7
                    if score >= 270:
                        star_achievement = 8
                    if score >= 285:
                        star_achievement = 9
                    if score >= 290:
                        star_achievement = 10
                    if score >= 295:
                        star_achievement = 11
                elif distance == 18 and target == 40:
                    if score >= 190:
                        star_achievement = 6
                    if score >= 240:
                        star_achievement = 7
                    if score >= 260:
                        star_achievement = 8
                    if score >= 280:
                        star_achievement = 9
                    if score >= 285:
                        star_achievement = 10
                    if score >= 290:
                        star_achievement = 11
                # else:
                # form.errors.distance = "not distance and target combination"
            elif bow == 'compound':
                if distance == 9 and target == 40:
                    if score >= 50:
                        star_achievement = 1
                    if score >= 100:
                        star_achievement = 2
                    if score >= 150:
                        star_achievement = 3
                    if score >= 200:
                        star_achievement = 4
                elif distance == 18 and target == 40:
                    if score >= 30:
                        star_achievement = 2
                    if score >= 50:
                        star_achievement = 3
                    if score >= 100:
                        star_achievement = 4
                    if score >= 150:
                        star_achievement = 5
                    if score >= 200:
                        star_achievement = 6
                    if score >= 240:
                        star_achievement = 7
                    if score >= 260:
                        star_achievement = 8
                    if score >= 285:
                        star_achievement = 9
                    if score >= 290:
                        star_achievement = 10
                    if score >= 295:
                        star_achievement = 11
                # else:
                # form.errors.distance = "not distance and target combination"
            # else:
            # form.errors.bow = 'Not Valid Bow'
            # form.errors.catagory = 'JOAD Indoor'
        elif category == 'adult_indoor':
            # if distance == 9: form.errors.distance = 'Invalid Distance'
            # if target == 60: form.errors.target = 'Invalid Target'
            if bow == 'barebow':
                if score >= 70:
                    star_achievement = 1
                if score >= 100:
                    star_achievement = 2
                if score >= 120:
                    star_achievement = 3
                if score >= 150:
                    star_achievement = 4
                if score >= 175:
                    star_achievement = 5
                if score >= 200:
                    star_achievement = 6
                if score >= 225:
                    star_achievement = 7
                if score >= 240:
                    star_achievement = 8
                if score >= 250:
                    star_achievement = 9
                if score >= 260:
                    star_achievement = 10
                if score >= 270:
                    star_achievement = 11
            elif bow == 'olympic':
                if score >= 90: star_achievement = 1
                if score >= 140: star_achievement = 2
                if score >= 190: star_achievement = 3
                if score >= 210: star_achievement = 4
                if score >= 230: star_achievement = 5
                if score >= 250: star_achievement = 6
                if score >= 265: star_achievement = 7
                if score >= 270: star_achievement = 8
                if score >= 285: star_achievement = 9
                if score >= 290: star_achievement = 10
                if score >= 295: star_achievement = 11
            elif bow == 'compound':
                if score >= 125:
                    star_achievement = 2  # TODO check this is it supposed to be 1?
                if score >= 150:
                    star_achievement = 2
                if score >= 175:
                    star_achievement = 3
                if score >= 200:
                    star_achievement = 4
                if score >= 220:
                    star_achievement = 5
                if score >= 240:
                    star_achievement = 6
                if score >= 260:
                    star_achievement = 7
                if score >= 270:
                    star_achievement = 8
                if score >= 280:
                    star_achievement = 9
                if score >= 285:
                    star_achievement = 10
                if score >= 290:
                    star_achievement = 11
        # else:
        # form.errors.catagory = 'Not Indoor'
        return star_achievement

    def get_dict(self):
        return self.ps_dict

    def record_shoot(self):
        # log information into database
        m = self.ps_dict['wpa_membership_number']
        if m == "":
            m = None
        s = f"INSERT INTO `pin_shoot` (`first_name`, `last_name`, `club`, `category`, `bow`, " \
            f"`shoot_date`, `distance`, `target`, `stars`, `wpa_membership_number`, `score`) VALUES (" \
            f"'{self.ps_dict['first_name']}', '{self.ps_dict['last_name']}', '{self.ps_dict['club']}', " \
            f"'{self.ps_dict['category']}', '{self.ps_dict['bow']}', '{self.ps_dict['shoot_date']}', " \
            f"'{self.ps_dict['distance']}', '{self.ps_dict['target']}', '{self.ps_dict['stars']}', " \
            f" %s, '{self.ps_dict['score']}')"

        self.db.execute(s, (m,))

    def set_dict(self, d):
        self.ps_dict = d

# calculate_pins(psd['category'], psd['bow'], psd['target'], psd['distance'], psd['score'])

if __name__ == '__main__':
    PinShoot(None)
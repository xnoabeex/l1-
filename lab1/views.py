from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        informsstud = []
        otlich = []
        otchis = []
        people = Student([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         ['Ажель Н.В.', 'Андреева Ю.В.', 'Бандеев Х.А.', 'Власенко А.В.', 'Газизов Р.Р.',
                          'Зуев А.С.', 'Киселев А.С.', 'Кудряшова А.О.', 'Кузнецова А.С.', 'Култаев П.И.'])
        predmet = Subject(['timp', 'tvims', 'philosophy', 'english', 'sport'])
        ocenka = Score([[2, 2, 2, 3, 2], [5, 5, 5, 5, 5], [4, 5, 4, 4, 4],
                        [2, 2, 2, 2, 3], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5],
                        [2, 3, 2, 2, 2], [2, 3, 3, 3, 2], [5, 5, 5, 5, 5],
                        [2, 2, 2, 3, 3]], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

        for i in range(1, 11):
            stats = Statistics(ocenka.insert_ocenki(i))
            informsstud.append(stats.zapis(
                i, people.insert_inicial(i), predmet.insert_predmett()))
            otlich = '; '.join(people.insert_inicial(i)
                               for i in ocenka.excellent_student())
            otchis = '; '.join(people.insert_inicial(i)
                               for i in ocenka.bed_student())

        context.update(
            {
                'students_statistics': informsstud,
                'excellent_students': otlich,
                'bad_students': otchis
            }
        )

        return context


class Student:

    def __init__(self, peoples_n, inicial):
        self.peoples = dict(zip(peoples_n, inicial))

    def insert_inicial(self, peoples_n):
        return self.peoples.setdefault(peoples_n)


class Statistics:

    def __init__(self, ocenki):
        self.ocenki = ocenki

    def sred(self):
        return float(sum(self.ocenki)) / len(self.ocenki)

    def zapis(self, peoples_n, inicial, predmett):
        inform = {'id': peoples_n, 'fio': inicial}
        op = dict(zip(predmett, self.ocenki))
        inform.update(op)
        inform.update({'sredznach': self.sred()})
        return inform


class Subject:

    def __init__(self, predmett):
        self.predmett = predmett

    def insert_predmett(self):
        return self.predmett


class Score:

    def __init__(self, ocenki, peoples_n):
        self.student_ocenkis = dict(zip(peoples_n, ocenki))

    def insert_ocenki(self, peoples_n):
        return self.student_ocenkis.setdefault(peoples_n)

    def bed_student(self):
        op = self.student_ocenkis.items()
        return [i[0] for i in op if i[1].count(2)]

    def excellent_student(self):
        op = self.student_ocenkis.items()
        return [i[0] for i in op if i[1].count(5) == len(i[1])]

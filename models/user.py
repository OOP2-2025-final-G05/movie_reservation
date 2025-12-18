from peewee import Model, CharField, IntegerField
from .db import db

class User(Model):
    name = CharField()
    age = IntegerField()
    category = CharField(default="未分類")  # ★追加

    class Meta:
        database = db

    @staticmethod
    def judge_category(age: int) -> str:
        """年齢から区分を判定"""
        if age < 13:
            return "子供"
        elif age < 65:
            return "大人"
        else:
            return "シニア"

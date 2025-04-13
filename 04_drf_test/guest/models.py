from django.db import models


def get_weekday_jp(date):
    """
    指定した日付の曜日を日本語で返す（例：月、火、水、...）
    """
    if date is None:
        return ""
    return ["月", "火", "水", "木", "金", "土", "日"][date.weekday()]


class Guest(models.Model):
    """利用者情報"""

    name = models.CharField(max_length=50, verbose_name="氏名")
    birthday = models.DateField(null=True, blank=True, verbose_name="生年月日")
    contact = models.CharField(max_length=100, blank=True, verbose_name="連絡先")
    notes = models.TextField(blank=True, null=True, verbose_name="備考")

    class Meta:
        verbose_name = "利用者情報"
        verbose_name_plural = "利用者情報"

    def __str__(self):
        return self.name


class VisitType(models.Model):
    """来訪種別（泊、通い、休み など）"""

    code = models.CharField(
        max_length=10, unique=True, verbose_name="コード"
    )  # 例：泊、通い、休
    name = models.CharField(
        max_length=50, verbose_name="来訪種別"
    )  # 例：泊まり、通い、休み
    color = models.CharField(max_length=10, default="#cccccc", verbose_name="色コード")

    class Meta:
        verbose_name = "来訪種別"
        verbose_name_plural = "来訪種別"

    def __str__(self):
        return f"{self.code}（{self.name}）"


class VisitSchedule(models.Model):
    """利用者の来訪スケジュール（1人1日1件）"""

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="利用者")
    visit_type = models.ForeignKey(
        VisitType, on_delete=models.SET_NULL, null=True, verbose_name="来訪種別"
    )
    date = models.DateField(verbose_name="日付")
    arrive_time = models.TimeField(verbose_name="来所時間", null=True)
    leave_time = models.TimeField(verbose_name="帰宅時間", null=True)
    note = models.TextField(blank=True, null=True, verbose_name="備考")

    @property
    def weekday_jp(self):
        """
        指定した日付の曜日を日本語で返す
        """
        return get_weekday_jp(self.date)

    class Meta:
        unique_together = ("guest", "date")
        ordering = ["date"]
        verbose_name = "来訪スケジュール"
        verbose_name_plural = "来訪スケジュール"

    def __str__(self):
        return f"{self.date} - {self.guest.name} - {self.visit_type.code if self.visit_type else '未定'}"

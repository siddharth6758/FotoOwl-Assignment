from django.db import models
from user_account.models import CustomUser
from books.models import Books

# Create your models here.
REQUEST_STATUS = (
    ('pending','PENDING'),
    ('completed','COMPLETED')
)
class LibraryManagement(models.Model):
    borrow_by = models.ForeignKey(CustomUser,related_name='borrow_by',on_delete=models.CASCADE)
    borrow_on = models.DateTimeField("Borrowed On",auto_now_add=True)
    book_borrowed = models.ForeignKey(Books,on_delete=models.CASCADE)
    borrow_till = models.DateTimeField("Borrowed Till")
    is_approved = models.BooleanField("Is Approved",default=False)
    decision_by = models.ForeignKey(CustomUser,related_name='decision_by',on_delete=models.CASCADE,null=True,blank=True)
    request_status = models.CharField("Status",max_length=100,choices=REQUEST_STATUS,default='pending',null=True,blank=True)

    def __str__(self):
        return f"{self.book_borrowed} request by {self.borrow_by}"

    class Meta:
        verbose_name_plural = "LibraryManagement"
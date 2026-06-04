from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Member, Court, Schedule, Membership, Announcement,Payment

# 1. Main Dashboard View
@login_required
def index(request):
    recent_members = Member.objects.all().order_by('-id')[:3]
    member_count = Member.objects.count()
    context = {
        'recent_members': recent_members,
        'member_count': member_count,
    }
    return render(request, 'members/index.html', context)

# 2. About View
def about(request):
    return render(request, 'members/about.html')

# 3. Details View
@login_required
def details(request, id):
    mymember = Member.objects.get(id=id)
    context = {
        'member': mymember,
    }
    return render(request, 'members/details.html', context)

# 4. Add Member View
# Fix 2: Save phone and joined_date in the add view
# @login_required
def add(request):
    if request.method == 'POST':
        firstname = request.POST['first']
        lastname = request.POST['last']
        phone = request.POST.get('phone', '')
        joined_date = request.POST.get('joined_date') or None

        member = Member(
            firstname=firstname,
            lastname=lastname,
            phone=phone or None,
            joined_date=joined_date,
        )
        member.save()
        return redirect('members')
    return render(request, 'members/add.html')

# 5. Delete Member View
@login_required
def delete(request, id):
    member = Member.objects.get(id=id)
    if request.method == 'POST':
        member.delete()
        return redirect('members')
    context = {
        'member': member,
    }
    return render(request, 'members/delete_confirm.html', context)

# 6. Edit Member View
@login_required
def edit(request, id):
    member = Member.objects.get(id=id)
    if request.method == 'POST':
        member.firstname = request.POST['firstname']   # was 'first'
        member.lastname = request.POST['lastname']     # was 'last'
        member.phone = request.POST.get('phone') or None        # was missing
        member.joined_date = request.POST.get('joined_date') or None  # was missing
        member.save()
        return redirect('members')
    context = {
        'member': member,
    }
    return render(request, 'members/edit.html', context)

# 7. Members List View
@login_required
def members_list(request):
    query = request.GET.get('search', '')
    if query:
        all_members = Member.objects.filter(
            firstname__icontains=query
        ) | Member.objects.filter(
            lastname__icontains=query
        )
    else:
        all_members = Member.objects.all()
    context = {
        'mymembers': all_members,
        'query': query,
    }
    return render(request, 'members/list.html', context)

# 8. Stats View
@login_required
def stats(request):
    total = Member.objects.count()
    newest = Member.objects.order_by('-joined_date').first()
    oldest = Member.objects.order_by('joined_date').first()
    this_year = Member.objects.filter(joined_date__year=timezone.now().year).count()
    no_phone = Member.objects.filter(phone__isnull=True).count()
    context = {
        'total': total,
        'newest': newest,
        'oldest': oldest,
        'this_year': this_year,
        'no_phone': no_phone,
    }
    return render(request, 'members/stats.html', context)

# 9. Courts View
@login_required
def courts(request):
    all_courts = Court.objects.all()
    context = {
        'courts': all_courts,
    }
    return render(request, 'members/courts.html', context)

# 10. Schedule View
@login_required
def schedule(request):
    all_sessions = Schedule.objects.all().order_by('date', 'time')
    context = {
        'sessions': all_sessions,
    }
    return render(request, 'members/schedule.html', context)

# 11. Membership View
@login_required
def membership(request):
    all_memberships = Membership.objects.select_related('member').all()
    context = {
        'memberships': all_memberships,
    }
    return render(request, 'members/membership.html', context)

# 12. Announcements View
@login_required
def announcements(request):
    all_announcements = Announcement.objects.all().order_by('-date_posted')
    context = {
        'announcements': all_announcements,
    }
    return render(request, 'members/announcements.html', context)

# 13. Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/members/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 14. Payments View@login_required
def payments(request):
    all_payments = Payment.objects.select_related('member').order_by('-date')
    total_paid = Payment.objects.filter(status='paid').aggregate(models.Sum('amount'))['amount__sum'] or 0
    total_pending = Payment.objects.filter(status='pending').aggregate(models.Sum('amount'))['amount__sum'] or 0
    context = {
        'payments': all_payments,
        'total_paid': total_paid,
        'total_pending': total_pending,
    }
    return render(request, 'members/payments.html', context)

@login_required
def add_payment(request):
    members = Member.objects.all()
    if request.method == 'POST':
        member_id = request.POST['member']
        payment_type = request.POST['payment_type']
        method = request.POST['method']
        amount = request.POST['amount']
        status = request.POST['status']
        notes = request.POST.get('notes', '')
        member = Member.objects.get(id=member_id)
        Payment.objects.create(
            member=member,
            payment_type=payment_type,
            method=method,
            amount=amount,
            status=status,
            notes=notes
        )
        return redirect('payments')
    context = {'members': members}
    return render(request, 'members/add_payment.html', context)

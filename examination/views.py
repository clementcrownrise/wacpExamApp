from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Examination
from letter.models import Letter
from faculty.models import Faculty
from . forms import ExamForm


# Create your views here.

def selected(request):
    if request.method == 'POST':
        faculty = request.POST.get('faculty')
        results  = Letter.objects.filter(faculty__icontains=faculty)
        #return HttpResponse(results)
        return render(request, "examination/examDetails.html", {'results': results})



@login_required
def index(request):
    #return HttpResponse("All created exams would be listed here")
    examinations = Examination.objects.order_by('-id')
    paginator = Paginator(examinations, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "examination/index.html",
                  {'examinations':examinations,'page_obj': page_obj})

@login_required
def exam_details(request, examination_id):
    faculties = Faculty.objects.all()
    examination = get_object_or_404(Examination, id=examination_id)

    # Get letters related to the examination
    letters = Letter.objects.filter(examination_id=examination_id)

    # Paginate the letters (20 per page)
    paginator = Paginator(letters, 50)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # If page is not an integer, show first page
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # If out of range, show last page

    return render(request, "examination/examDetails.html", {
        'examination': examination,
        'page_obj': page_obj,  # Pass only paginated data
        'faculties': faculties
    })

@login_required
def deleteExam(request, examination_id):
    examination = get_object_or_404(Examination, id=examination_id)

    if request.method == 'POST':
        examination.delete()
        messages.success(request, "Examination was deleted successfully")  
        return redirect('examination:index')
    return render(request, 'examination/confirmDelete.html',{'examination':examination})
    #return HttpResponse("All deleted")

@login_required
def examEdit(request, examination_id):
    examination = get_object_or_404(Examination, id=examination_id)

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=examination)
        if form.is_valid():
            form.save()
            messages.success(request, "Examination was updated successfully")  
            return redirect('examination:index')
    else:
        form = ExamForm(instance=examination)
    return render(request, 'examination/examEdit.html',
                      {'form': form, 'examination':examination})


@login_required
def createExam(request):
    #return HttpResponse("I am being served for creating of exams");
    if request.method == 'POST':
        
        form = ExamForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Examination was created successfully")  
            return redirect('examination:index')
    else:
        form = ExamForm()
    return render(request, "examination/createExam.html",
                  {'form': form})




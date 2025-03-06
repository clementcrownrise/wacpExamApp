from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives #for email sending
from django.template.loader import render_to_string #for sending email
from django.utils.html import strip_tags  #for sending email
from django.db.models import Q 
from django.conf import settings
import pandas as pd
from django.contrib import messages
from . forms import ExcelUploadForm
from .models import Letter
from . models import Examination
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
import tempfile
import mimetypes
from django.core.mail import EmailMessage
from faculty.models import Faculty
from .forms import SearchForm
import os

# Create your views here.
@login_required
def index(request):
    examinations = Examination.objects.all()
    faculties = Faculty.objects.all()
    form = SearchForm(request.POST)
    letters = Letter.objects.none()
    page_obj = None 


    if request.method == 'POST':
            if form.is_valid():
                #return HttpResponse('am ai getting the right thing')
                examination = request.POST.get('examination')
                faculty =request.POST.get('faculty')
                letters = Letter.objects.filter(Q(examination_id = examination)
                                         & Q(faculty__icontains=faculty))
                #return HttpResponse(faculty)
                paginator = Paginator(letters, 20)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number) 
                
    return render(request, 'letter/index.html',
                  {'letters':letters ,
                   'form': form,
                    'page_obj': page_obj,
                   'faculties': faculties,
                   'examinations':examinations})




@login_required
def mailSample(request, letter_id):
    letter = get_object_or_404(Letter, id=letter_id)
    #return HttpResponse(letter)
    return render(request, 'letter/mailsample.html',{'letter': letter})

@login_required
def deleteAll(request):
    records = Letter.objects.all()
    if records.delete():
        return HttpResponse("All records deleted")
    
@login_required
def letterDetails(request, letter_id):
    letter  = get_object_or_404(Letter, id=letter_id)
    return render(request, 'letter/details.html', {'letter': letter})


#This will uplload excel file for me
@login_required
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST,request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            requestedExaminationId = request.POST.get('examination')
            #i willl read excel file now
            df = pd.read_excel(excel_file)

            #iterate thrrough rows
            for _, row in df.iterrows():
                Letter.objects.create(
                    examination_id = requestedExaminationId,
                    surname=row['Surname'],
                    name = row['Name'],
                    institutionAddress = row['InstitutionAddress'],
                    role = row['Role'],
                    membershipOrFellowship = row['MembershipOrFellowship'],
                    hotel = row['Hotel'],
                    centerOfTheExamination = row['CenterOfTheExamination'],
                    meal = row['Meal'],
                    cc = row['CC'],
                    arrivalDate = row['ArrivalDate'],
                    depatureDate = row['DepatureDate'],
                    email = row['Email'],
                    faculty = row['Faculty'],
                    onOrBefore = row['OnOrBefore'],
                    holdAt = row['HoldAt'],
                    countryOfTheExamination = row['CountryOfTheExamination'],
                    InstitutionAddressCountry = row['InstitutionAddressCountry'],

                )
            #return HttpResponse('Data Imported Successfully!')
            messages.success(request, "Records successfully imported")  
            return redirect('examination:index')
    else:
        form =ExcelUploadForm()
    examinations = Examination.objects.all()
    
    return render(request, 'letter/create.html',{'form':form,'examinations':examinations})


def send_personalized_email(request):
   
    #letters = Letter.objects.all()  # Fetch all users
    #letters = Letter.objects.all() #.values('email')  # Fetch first Letter instance
    letters = Letter.objects.filter(examination_id = 5)
    #return HttpResponse(letters)
    #letters = ['clementcrownrise@gmail.com','clementcrownrise@yahoo.com']
    for letter in letters:
        #return HttpResponse(letter.email)
        pdf_buffer = generate_pdf(letter.email)  # Generate a PDF for the user
        
        if not pdf_buffer:
            print(f"Failed to generate PDF for {letter}")
            continue  # Skip this user if PDF generation fails
        
        # Email details
        subject = "Your Personalized Document"
        html_message = render_to_string('emails/email_template.html', {'letter': letter})
        plain_message = strip_tags(html_message)  # Convert HTML to plain text
        email = EmailMessage(
            subject,
            plain_message,
            'info@wacp-coam',  # Replace with your sender email
            [email],  # Assuming Letter model has an 'email' field
        )
        
        # Attach the PDF
        email.attach(f"document_{letter.id}.pdf", pdf_buffer.getvalue(), "application/pdf")
        
        # Send email
        email.send()
        print(f"Email sent to {letter.email}")

    print("All emails have been processed.")






@login_required
def createLetter(request):
    pass
    #return HttpResponse("this is for letter creation")
   # return render(request, 'letter/create.html')

#this triggers the mail
@login_required
def send_letter_view(request):
    #sendLetter() the main one that sends letter
    return HttpResponse("Emails have been sent!")

def generate_pdf(letter):

    """Generates a PDF from the letter template"""
    html_content = render_to_string("emails/attachment.html", {"letter": letter})
    pdf_file = BytesIO()
    
    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
    if pisa_status.err:
        return None
    
    pdf_file.seek(0)  # Reset file pointer to start
    return pdf_file



@login_required
def sendLetter(request):
    examination = request.POST.get('examination')
    facultyName = request.POST.get('faculty')
    letters = Letter.objects.filter(Q(examination_id = examination)
                                         & Q(faculty__icontains=facultyName))

    #return HttpResponse(letters)
    examination = Examination.objects.get(id = examination)
    subject = examination.examName
    #return HttpResponse(examination.examName)
    totFlyer = examination.totFlyers
    #return HttpResponse(totFlyer)
    #timetableIbadan = 'media/uploads/'
    #timetableAccra = 'media/uploads/'
    #timetableAbuja= 'media/uploads/'
    #travelProtocol = 'media/uploads/'
    #totFlyer = 'media/uploads/'

    pdf_files = [examination.timetableAbuja,
                  examination.timetableAccra, 
                  examination.timetableIbadan,
                ]
    foreign_pdf_files = [examination.timetableAbuja,
                  examination.timetableAccra, 
                  examination.timetableIbadan,
                examination.travelProtocol]
    

    
    for letter in letters:
        html_message = render_to_string("emails/letter_template.html", {"letter": letter})
        plain_message = strip_tags(html_message)  # Remove HTML for plain text version
         

        email = EmailMultiAlternatives(
            subject,
            plain_message,  # Plain text content
            request.user.username or "adeyemi.tosin@wacpcoam.org" , # Or any other valid email
            [letter.email],  # Recipient list
        )
        email.attach_alternative(html_message, "text/html")  # Attach HTML content

        #i attached the generated guys here
        pdf_file = generate_pdf(letter)
        if pdf_file:
            email.attach(f"Invitation_Letter_{letter.surname}.pdf", pdf_file.getvalue(), "application/pdf")

        if  letter.InstitutionAddressCountry != letter.countryOfTheExamination:                
            for foreign_pdf_file in foreign_pdf_files:
                with open(foreign_pdf_file.path, "rb") as f:
                    email.attach(os.path.basename(foreign_pdf_file.path),
                                  f.read(),
                                  "application/pdf")                
        else:   
            for pdf_file in pdf_files:
                with open(pdf_file.path, "rb") as f:
                    email.attach(os.path.basename(pdf_file.path),
                                  f.read(), "application/pdf")
        if totFlyer :
            image_path = examination.totFlyers.path
            image_name = examination.totFlyers.name
            file_type, _ = mimetypes.guess_type(image_path)  # Get correct content type
            with open(image_path, 'rb') as img:
                email.attach(image_name, img.read(), file_type) 
        email.send()  #
    
    return HttpResponse("Emails have been sent!")

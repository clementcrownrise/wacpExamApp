from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives #for email sending
from django.template.loader import render_to_string #for sending email
from django.utils.html import strip_tags  #for sending email
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

# Create your views here.
@login_required
def index(request):
    #with open("output.pdf", "wb") as pdf_file:
       #pisa.CreatePDF("<h1>Hello</h1>", pdf_file)

    examinations = Examination.objects.all()
    if request.method == 'POST':
        examinations = request.POST.get('examination')
        #return HttpResponse(examination)
        letters = Letter.objects.filter(examination_id = examinations)
        paginator = Paginator(letters, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number) 

    else:
        examinations = Examination.objects.all()
        letters = Letter.objects.all()
        paginator = Paginator(letters, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number) 
    return render(request, 'letter/index.html',{'letters':letters ,'page_obj': page_obj,'examinations':examinations})


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

                )
            #return HttpResponse('Data Imported Successfully!')
            messages.success(request, "Records successfully imported")  
            return redirect('examination:index')
    else:
        form =ExcelUploadForm()
    examinations = Examination.objects.all()
    
    return render(request, 'letter/create.html',{'form':form,'examinations':examinations})

@login_required
def generate_pdf(letter):
    template = get_template("emails/pdf_template.html")
    html = template.render({'email': letter.email})  # ✅ Correct: Use `letter.email`
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html, dest=pdf_buffer)
    return pdf_buffer

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






@login_required
def sendLetter(request, id):
    examination = Examination.objects.get(id=id)
    #return HttpResponse(examination)
    letters = Letter.objects.filter(examination_id = id)  # Get all letter for a particular examination in the database
    subject = examination
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
            "info@wacp-coam.org",  # From email
            [letter.email],  # Recipient list
        )
        email.attach_alternative(html_message, "text/html")  # Attach HTML content
        examCenters = ['Abuja','Enugu','Ibadan']
        if not letter.centerOfTheExamination in examCenters:                
            for foreign_pdf_file in foreign_pdf_files:
                if foreign_pdf_file:
                    email.attach(foreign_pdf_file.name, foreign_pdf_file.read(),"application/pdf")                
        else:   
            for pdf_file in pdf_files:
                if pdf_file:
                    email.attach(pdf_file.name, pdf_file.read(), "application/pdf")

       
        image_path = examination.totFlyers.path
        image_name = examination.totFlyers.name
        file_type, _ = mimetypes.guess_type(image_path)  # Get correct content type
        with open(image_path, 'rb') as img:
            email.attach(image_name, img.read(), file_type) 
        email.send()  #
    
    return HttpResponse("Emails have been sent!")

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PresentationForm
from .models import PresentationData
from pptx import Presentation
from django.http import HttpResponse, FileResponse
import pandas as pd
import io
import tempfile

from django.http import FileResponse
from django.shortcuts import render
from .forms import PresentationForm
from .models import PresentationData

from django.http import FileResponse
from django.shortcuts import render
from .forms import PresentationForm
from .models import PresentationData

import os
from pptx import Presentation
import win32com.client
import pythoncom

from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_superuser)(view_func)


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')

@superuser_required
def create_presentation(request):
    if request.method == "POST":
        form = PresentationForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()  # Save first to generate entry_id

            # Split AP field if needed
            ap_value = form.cleaned_data.get('ap', '')
            ap_parts = ap_value.split(' ', 1)
            data.ap1 = ap_parts[0]
            data.ap2 = ap_parts[1] if len(ap_parts) > 1 else ''
            data.save()

            template_path = "Presentation1.pptx"
            # Sanitize toname for safe filename; adjust as needed
            safe_toname = ''.join(c if c.isalnum() else '_' for c in str(data.toname))
            out_pptx_path = f"tmp_{safe_toname}.pptx"
            out_png_path = f"{safe_toname}_slide.png"

            # Add entry_id replacement with key 'idno'
            replace_map = {
                "date": data.date.strftime('%d-%m-%Y'),
                "toname": data.toname,
                "phno": data.phno,
                "aadharno": data.aadharno,
                "ap1": data.ap1,
                "ap2": data.ap2,
                "aptdas": data.aptdas,
                "idno": str(data.entry_id),  # The placeholder in your PPTX
            }

            # Edit PPTX
            prs = Presentation(template_path)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for para in shape.text_frame.paragraphs:
                            for run in para.runs:
                                for key, val in replace_map.items():
                                    if key in run.text:
                                        run.text = run.text.replace(key, val)

            prs.save(out_pptx_path)

            # Export slide as PNG
            pythoncom.CoInitialize()
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            presentation = powerpoint.Presentations.Open(os.path.abspath(out_pptx_path), WithWindow=True)
            presentation.Slides(1).Export(os.path.abspath(out_png_path), "PNG")
            presentation.Close()
            powerpoint.Quit()
            pythoncom.CoUninitialize()

            response = FileResponse(
                open(out_png_path, "rb"),
                content_type="image/png"
            )
            response['Content-Disposition'] = f'attachment; filename="{safe_toname}_slide.png"'
            return response
    else:
        form = PresentationForm()
    return render(request, "presentation_form.html", {"form": form})


from django.shortcuts import render
from .models import PresentationData
@superuser_required
def track_history(request):
    query = request.GET.get('search_id', '').strip()
    entries = PresentationData.objects.all().order_by('-created_at')
    search_result = None
    not_found = False
    
    if query:
        search_result = entries.filter(entry_id=query)
        if not search_result.exists():
            not_found = True
    else:
        search_result = entries
    
    return render(request, 'history.html', {
        'entries': search_result,
        'search_term': query,
        'not_found': not_found
    })

@superuser_required
def export_excel(request):
    entries = PresentationData.objects.all().values(
        'entry_id', 'date', 'toname', 'phno', 'aadharno', 'ap1', 'ap2', 'aptdas', 'created_at'
    )
    import pandas as pd

    df = pd.DataFrame(entries)

    # Convert datetimes to strings (or remove tz info)
    if 'created_at' in df.columns:
        df['created_at'] = df['created_at'].apply(
            lambda dt: dt.strftime('%d-%m-%Y %H:%M') if hasattr(dt, 'strftime') else str(dt)
        )
    if 'date' in df.columns:
        df['date'] = df['date'].apply(
            lambda d: d.strftime('%d-%m-%Y') if hasattr(d, 'strftime') else str(d)
        )

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Presentations')
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="presentation_history.xlsx"'
    return response


from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import PresentationData
import os
from pptx import Presentation
import win32com.client
import pythoncom

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import PresentationData
import os
from pptx import Presentation
import win32com.client
import pythoncom
@superuser_required
def history_download_png(request, pk):
    pk=str(pk).upper()
    entry = get_object_or_404(PresentationData, pk=pk)
    safe_entry_id = ''.join(c if c.isalnum() else '_' for c in str(entry.entry_id))
    template_path = "Presentation1.pptx"
    out_pptx_path = f"tmp_{safe_entry_id}.pptx"
    out_png_path = f"{safe_entry_id}_slide.png"

    replace_map = {
        "date": entry.date.strftime('%d-%m-%Y'),
        "toname": entry.toname,
        "phno": entry.phno,
        "aadharno": entry.aadharno,
        "ap1": entry.ap1,
        "ap2": entry.ap2,
        "aptdas": entry.aptdas,
        "idno": str(entry.entry_id),  # Use 'idno' placeholder in PPTX
    }

    prs = Presentation(template_path)
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        for key, val in replace_map.items():
                            if key in run.text:
                                run.text = run.text.replace(key, str(val))
    prs.save(out_pptx_path)

    pythoncom.CoInitialize()
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    presentation = powerpoint.Presentations.Open(os.path.abspath(out_pptx_path), WithWindow=True)
    presentation.Slides(1).Export(os.path.abspath(out_png_path), "PNG")
    presentation.Close()
    powerpoint.Quit()
    pythoncom.CoUninitialize()

    response = FileResponse(open(out_png_path, "rb"), content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="{safe_entry_id}_slide.png"'
    return response

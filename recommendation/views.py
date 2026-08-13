
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import HouseboatForm
import json
from django.http import JsonResponse
from django.shortcuts import render
from .rag import ask_rag
from .models import (
    ProfessionalHouseboatDataset500Rows,
    Booking,
    Wishlist,
    ContactMessage
)

from .forms import BookingForm

from .ai import (
    get_recommendations,
    get_personalized_recommendations
)


# =========================================================
# HELPER FUNCTION - ASSIGN HOUSEBOAT IMAGE
# =========================================================

def assign_houseboat_image(boat):
    """
    Assign one of the 12 available houseboat images
    based on the Houseboat ID.

    Example:
    HB0001 -> HB0001.jpg
    HB0012 -> HB0012.jpg
    HB0013 -> HB0001.jpg
    HB0014 -> HB0002.jpg
    """

    try:
        boat_number = int(
            str(boat.houseboatid).replace("HB", "")
        )

        image_number = (
            (boat_number - 1) % 12
        ) + 1

        boat.image_file = (
            f"HB{image_number:04d}.jpg"
        )

    except (ValueError, TypeError):
        boat.image_file = "HB0001.jpg"

    return boat


# =========================================================
# ADMIN DASHBOARD
# =========================================================

# =========================================================
@login_required(login_url="login")
def admin_dashboard(request):

    # -----------------------------------------
    # ADMIN ACCESS CHECK
    # -----------------------------------------

    if not request.user.is_staff:
        messages.error(
            request,
            "You are not authorized to access the Admin Dashboard."
        )
        return redirect("home")


    # -----------------------------------------
    # BASIC STATISTICS
    # -----------------------------------------

    total_houseboats = (
        ProfessionalHouseboatDataset500Rows.objects.count()
    )

    total_users = User.objects.count()

    total_bookings = Booking.objects.count()

    total_wishlist = Wishlist.objects.count()


    # -----------------------------------------
    # CONTACT MESSAGE STATISTICS
    # -----------------------------------------

    total_contact_messages = (
        ContactMessage.objects.count()
    )

    unread_contact_messages = (
        ContactMessage.objects
        .filter(is_read=False)
        .count()
    )


    # -----------------------------------------
    # TOP BOOKED HOUSEBOATS
    # -----------------------------------------

    top_booked = (
        Booking.objects
        .values("houseboat")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    booked_labels = []

    booked_values = []


    for item in top_booked:

        try:

            boat = (
                ProfessionalHouseboatDataset500Rows.objects
                .get(
                    houseboatid=item["houseboat"]
                )
            )

            booked_labels.append(
                boat.houseboatname
            )

            booked_values.append(
                item["total"]
            )

        except ProfessionalHouseboatDataset500Rows.DoesNotExist:

            continue


    # -----------------------------------------
    # TOP WISHLISTED HOUSEBOATS
    # -----------------------------------------

    top_wishlisted = (
        Wishlist.objects
        .values("houseboat")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    wishlist_labels = []

    wishlist_values = []


    for item in top_wishlisted:

        try:

            boat = (
                ProfessionalHouseboatDataset500Rows.objects
                .get(
                    houseboatid=item["houseboat"]
                )
            )

            wishlist_labels.append(
                boat.houseboatname
            )

            wishlist_values.append(
                item["total"]
            )

        except ProfessionalHouseboatDataset500Rows.DoesNotExist:

            continue

       # -----------------------------------------
    # BOOKING STATUS STATISTICS
    # -----------------------------------------

    pending_bookings = (
        Booking.objects.filter(
            status="Pending"
        ).count()
    )

    approved_bookings = (
        Booking.objects.filter(
            status="Approved"
        ).count()
    )

    rejected_bookings = (
        Booking.objects.filter(
            status="Rejected"
        ).count()
    )
    # -----------------------------------------
    # REVENUE ANALYTICS
    # -----------------------------------------

    total_revenue = 0

    approved_bookings = Booking.objects.filter(
       status="Approved"
)

    for booking in approved_bookings:

       try:

          boat = ProfessionalHouseboatDataset500Rows.objects.get(
            houseboatid=booking.houseboat
        )

          total_revenue += boat.priceinr

       except ProfessionalHouseboatDataset500Rows.DoesNotExist:
         continue
# -----------------------------------------
   # MOST BOOKED LOCATION
# -----------------------------------------

    most_booked_location = "N/A"

    location_counts = {}

    approved_bookings = Booking.objects.filter(
     status="Approved"
    )

    for booking in approved_bookings:

       try:

         boat = ProfessionalHouseboatDataset500Rows.objects.get(
            houseboatid=booking.houseboat
         )

         location = boat.location

         location_counts[location] = (
            location_counts.get(location, 0) + 1
         )

       except ProfessionalHouseboatDataset500Rows.DoesNotExist:
        continue


    if location_counts:


     most_booked_location = max(
        location_counts,
        key=location_counts.get
    )
   # -----------------------------------------
#   MOST POPULAR HOUSEBOAT
# -----------------------------------------

    most_popular_houseboat = "N/A"

    top_boat = (
      Booking.objects
      .filter(status="Approved")
      .values("houseboat")
      .annotate(total=Count("id"))
      .order_by("-total")
      .first()
    )

    if top_boat:


      try:

        boat = ProfessionalHouseboatDataset500Rows.objects.get(
            houseboatid=top_boat["houseboat"]
        )

        most_popular_houseboat = boat.houseboatname

      except ProfessionalHouseboatDataset500Rows.DoesNotExist:
        pass
    return render(
        request,
        "admin_dashboard.html",
        {
            "total_houseboats": total_houseboats,
            "total_users": total_users,
            "total_bookings": total_bookings,
            "total_wishlist": total_wishlist,

            "total_contact_messages": total_contact_messages,
            "unread_contact_messages": unread_contact_messages,

            "booked_labels": booked_labels,
            "booked_values": booked_values,

            "wishlist_labels": wishlist_labels,
            "wishlist_values": wishlist_values,

            "pending_bookings": pending_bookings,
            "approved_bookings": approved_bookings,
            "rejected_bookings": rejected_bookings,
            "total_revenue": total_revenue,
            "most_booked_location": most_booked_location,
            "most_popular_houseboat": most_popular_houseboat,

        }
    )
# =========================================================
# ADMIN - MANAGE HOUSEBOATS
# =========================================================

from django.db.models import Avg, Count

@login_required(login_url="login")
def admin_houseboats(request):

    if not request.user.is_staff:
        return redirect("home")

    search = request.GET.get("search")

    houseboats = ProfessionalHouseboatDataset500Rows.objects.all()

    if search:

        houseboats = houseboats.filter(
            houseboatname__icontains=search
        ) | houseboats.filter(
            location__icontains=search
        )

    luxury_count = ProfessionalHouseboatDataset500Rows.objects.filter(
        luxury="Yes"
    ).count()

    avg_rating = ProfessionalHouseboatDataset500Rows.objects.aggregate(
        Avg("rating")
    )["rating__avg"]

    total_locations = ProfessionalHouseboatDataset500Rows.objects.values(
        "location"
    ).distinct().count()

    return render(
        request,
        "admin_houseboats.html",
        {
            "houseboats": houseboats,
            "luxury_count": luxury_count,
            "avg_rating": round(avg_rating or 0, 1),
            "total_locations": total_locations,
        }
    )
# =========================================================
# ADMIN - MANAGE USERS
# =========================================================

@login_required(login_url="login")
def admin_users(request):

    if not request.user.is_staff:
        messages.error(
            request,
            "You are not authorized to access this page."
        )
        return redirect("home")

    users = (
        User.objects
        .all()
        .order_by("-date_joined")
    )

    return render(
        request,
        "admin_users.html",
        {
            "users": users
        }
    )


# =========================================================
# ADMIN - MANAGE BOOKINGS
# =========================================================

@login_required(login_url="login")
def admin_bookings(request):

    if not request.user.is_staff:
        messages.error(
            request,
            "You are not authorized to access this page."
        )
        return redirect("home")

    # Filter by booking status
    status = request.GET.get("status")

    bookings = Booking.objects.all()

    if status:
        bookings = bookings.filter(status=status)

    bookings = bookings.order_by("-id")

    return render(
        request,
        "admin_bookings.html",
        {
            "bookings": bookings,
            "selected_status": status,
        }
    )


# =========================================================
# ADMIN - MANAGE WISHLIST
# =========================================================

@login_required(login_url="login")
def admin_wishlist(request):

    if not request.user.is_staff:
        messages.error(
            request,
            "You are not authorized to access this page."
        )
        return redirect("home")

    wishlist = (
        Wishlist.objects
        .all()
        .order_by("-id")
    )

    return render(
        request,
        "admin_wishlist.html",
        {
            "wishlist": wishlist
        }
    )


# =========================================================
# USER DASHBOARD
# =========================================================

@login_required(login_url="login")
def user_dashboard(request):

    bookings = (
        Booking.objects
        .filter(user=request.user)
        .order_by("-id")
    )

    wishlist = (
        Wishlist.objects
        .filter(user=request.user)
        .order_by("-id")
    )

    recent_bookings = []


    for booking in bookings[:5]:

        try:

            boat = (
                ProfessionalHouseboatDataset500Rows.objects
                .get(
                    houseboatid=booking.houseboat
                )
            )

            assign_houseboat_image(boat)

            recent_bookings.append(
                {
                    "booking": booking,
                    "boat": boat
                }
            )

        except ProfessionalHouseboatDataset500Rows.DoesNotExist:
            continue


    return render(
        request,
        "user_dashboard.html",
        {
            "bookings": bookings,
            "wishlist": wishlist,

            "total_bookings":
                bookings.count(),

            "total_wishlist":
                wishlist.count(),

            "recent_bookings":
                recent_bookings,
        }
    )


# =========================================================
# HOME
# =========================================================

def home(request):

    houseboats = (
        ProfessionalHouseboatDataset500Rows.objects.all()
    )


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search = request.GET.get("search")

    if search:
        houseboats = houseboats.filter(
            location__icontains=search
        )


    # -----------------------------------------------------
    # PRICE FILTER
    # -----------------------------------------------------

    price = request.GET.get("price")

    if price:

        houseboats = houseboats.filter(
            priceinr__lte=price
        )


    # -----------------------------------------------------
    # AC FILTER
    # -----------------------------------------------------

    ac = request.GET.get("ac")

    if ac:

        houseboats = houseboats.filter(
            ac=ac
        )


    # -----------------------------------------------------
    # WIFI FILTER
    # -----------------------------------------------------

    wifi = request.GET.get("wifi")

    if wifi:

        houseboats = houseboats.filter(
            wifi=wifi
        )


    # -----------------------------------------------------
    # SORT
    # -----------------------------------------------------

    sort = request.GET.get("sort")

    if sort == "low":

        houseboats = houseboats.order_by(
            "priceinr"
        )

    elif sort == "high":

        houseboats = houseboats.order_by(
            "-priceinr"
        )


    # -----------------------------------------------------
    # ASSIGN IMAGES
    # -----------------------------------------------------

    for boat in houseboats:

        assign_houseboat_image(boat)


    return render(
        request,
        "home.html",
        {
            "houseboats": houseboats
        }
    )


# =========================================================
# HOUSEBOAT DETAILS + AI RECOMMENDATIONS
# =========================================================

def details(request, id):

    boat = get_object_or_404(
        ProfessionalHouseboatDataset500Rows,
        houseboatid=id
    )


    # Main image

    assign_houseboat_image(boat)


    # AI recommendations

    recommendations = (
        get_recommendations(id)
    )


    # Recommendation images

    for item in recommendations:

        recommended_boat = item["boat"]

        assign_houseboat_image(
            recommended_boat
        )


    return render(
        request,
        "details.html",
        {
            "boat": boat,
            "recommendations":
                recommendations
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register_page(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        email = request.POST.get(
            "email"
        )

        password = request.POST.get(
            "password"
        )


        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect(
                "register"
            )


        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        messages.success(
            request,
            "Registration successful!"
        )


        return redirect(
            "login"
        )


    return render(
        request,
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_page(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(
                request,
                user
            )


            # Redirect to originally requested page

            next_url = (
                request.POST.get("next")
                or request.GET.get("next")
            )


            if next_url:

                return redirect(
                    next_url
                )


            # Staff/Admin

            if (
                user.is_superuser
                or user.is_staff
            ):

                return redirect(
                    "admin_dashboard"
                )


            # Normal user

            return redirect(
                "user_dashboard"
            )


        else:

            messages.error(
                request,
                "Invalid username or password."
            )


    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_page(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect(
        "home"
    )


# =========================================================
# ABOUT
# =========================================================

def about(request):

    return render(
        request,
        "about.html"
    )


# =========================================================
# CONTACT
# =========================================================

def contact(request):

    if request.method == "POST":

        name = request.POST.get(
            "name"
        )

        email = request.POST.get(
            "email"
        )

        subject = request.POST.get(
            "subject"
        )

        message = request.POST.get(
            "message"
        )


        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )


        messages.success(
            request,
            "Thank you! Your message has been sent successfully."
        )


        return redirect(
            "contact"
        )


    return render(
        request,
        "contact.html"
    )


# =========================================================
# BOOK HOUSEBOAT
# =========================================================

@login_required(login_url="login")
def book(request, id):

    boat = get_object_or_404(
        ProfessionalHouseboatDataset500Rows,
        houseboatid=id
    )


    assign_houseboat_image(boat)


    if request.method == "POST":

        form = BookingForm(
            request.POST
        )


        if form.is_valid():

            booking = form.save(
                commit=False
            )

            booking.user = request.user

            booking.houseboat = (
                boat.houseboatid
            )

            booking.save()


            messages.success(
                request,
                "Houseboat booked successfully!"
            )


            return redirect(
                "my_bookings"
            )


    else:

        form = BookingForm()


    return render(
        request,
        "booking.html",
        {
            "boat": boat,
            "form": form
        }
    )


# =========================================================
# MY BOOKINGS
# =========================================================

@login_required(login_url="login")
def my_bookings(request):

    bookings = (
        Booking.objects
        .filter(
            user=request.user
        )
        .order_by("-id")
    )


    booking_list = []


    for booking in bookings:

        try:

            boat = (
                ProfessionalHouseboatDataset500Rows.objects
                .get(
                    houseboatid=booking.houseboat
                )
            )


            assign_houseboat_image(
                boat
            )


            booking_list.append(
                {
                    "booking": booking,
                    "boat": boat
                }
            )


        except ProfessionalHouseboatDataset500Rows.DoesNotExist:

            continue


    return render(
        request,
        "my_bookings.html",
        {
            "booking_list":
                booking_list
        }
    )


# =========================================================
# CANCEL BOOKING
# =========================================================

@login_required(login_url="login")
def cancel_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )


    booking.delete()


    messages.success(
        request,
        "Booking cancelled successfully."
    )


    return redirect(
        "my_bookings"
    )


# =========================================================
# ADD TO WISHLIST
# =========================================================

@login_required(login_url="login")
def add_wishlist(request, id):

    wishlist_item, created = (
        Wishlist.objects.get_or_create(
            user=request.user,
            houseboat=id
        )
    )


    if created:

        messages.success(
            request,
            "Added to Wishlist."
        )

    else:

        messages.info(
            request,
            "This houseboat is already in your Wishlist."
        )


    return redirect(
        "details",
        id=id
    )


# =========================================================
# MY WISHLIST
# =========================================================

@login_required(login_url="login")
def my_wishlist(request):

    wishlist = (
        Wishlist.objects
        .filter(
            user=request.user
        )
        .order_by("-id")
    )


    wishlist_list = []


    for item in wishlist:

        try:

            boat = (
                ProfessionalHouseboatDataset500Rows.objects
                .get(
                    houseboatid=item.houseboat
                )
            )


            assign_houseboat_image(
                boat
            )


            wishlist_list.append(
                {
                    "boat": boat,
                    "wish": item
                }
            )


        except ProfessionalHouseboatDataset500Rows.DoesNotExist:

            continue


    return render(
        request,
        "wishlist.html",
        {
            "wishlist_list":
                wishlist_list
        }
    )


# =========================================================
# REMOVE FROM WISHLIST
# =========================================================

@login_required(login_url="login")
def remove_wishlist(request, id):

    Wishlist.objects.filter(
        user=request.user,
        houseboat=id
    ).delete()


    messages.success(
        request,
        "Removed from Wishlist."
    )


    return redirect(
        "my_wishlist"
    )


# =========================================================
# PERSONALIZED AI RECOMMENDATIONS
# =========================================================

def recommend(request):

    recommendations = []


    if request.method == "POST":

        location = request.POST.get(
            "location"
        )

        max_price = request.POST.get(
            "max_price"
        )

        bedrooms = request.POST.get(
            "bedrooms"
        )

        capacity = request.POST.get(
            "capacity"
        )

        ac = request.POST.get(
            "ac"
        )

        wifi = request.POST.get(
            "wifi"
        )

        luxury = request.POST.get(
            "luxury"
        )


        recommendations = (
            get_personalized_recommendations(
                location=location,
                max_price=max_price,
                bedrooms=bedrooms,
                capacity=capacity,
                ac=ac,
                wifi=wifi,
                luxury=luxury
            )
        )


        for item in recommendations:

            boat = item["boat"]

            assign_houseboat_image(
                boat
            )


    return render(
        request,
        "recommend.html",
        {
            "recommendations":
                recommendations
        }
    )
# =========================================================
# ADMIN - CONTACT MESSAGES
# =========================================================

@login_required(login_url="login")
def admin_contact_messages(request):

    # Admin access check
    if not request.user.is_staff:

        messages.error(
            request,
            "You are not authorized to access Contact Messages."
        )

        return redirect("home")

    # Get all contact messages
    contact_messages = ContactMessage.objects.all().order_by("-created_at")

    # Statistics
    total_messages = contact_messages.count()

    unread_messages = contact_messages.filter(
        is_read=False
    ).count()

    read_messages = contact_messages.filter(
        is_read=True
    ).count()

    return render(
        request,
        "admin_contact_messages.html",
        {
            "contact_messages": contact_messages,
            "total_messages": total_messages,
            "unread_messages": unread_messages,
            "read_messages": read_messages,
        }
    )


# =========================================================
# MARK CONTACT MESSAGE AS READ
# =========================================================

@login_required(login_url="login")
def mark_contact_read(request, id):

    if not request.user.is_staff:

        messages.error(
            request,
            "You are not authorized to perform this action."
        )

        return redirect("home")

    contact_message = get_object_or_404(
        ContactMessage,
        id=id
    )

    contact_message.is_read = True

    contact_message.save()

    messages.success(
        request,
        "Message marked as read."
    )

    return redirect(
        "admin_contact_messages"
    )


# =========================================================
# DELETE CONTACT MESSAGE
# =========================================================

@login_required(login_url="login")
def delete_contact_message(request, id):

    if not request.user.is_staff:

        messages.error(
            request,
            "You are not authorized to perform this action."
        )

        return redirect("home")

    contact_message = get_object_or_404(
        ContactMessage,
        id=id
    )

    contact_message.delete()

    messages.success(
        request,
        "Contact message deleted successfully."
    )

    return redirect(
        "admin_contact_messages"
    )
# =========================================================
# =========================================================
# =========================================================
@login_required(login_url="login")
def approve_booking(request, id):

    if not request.user.is_staff:
        return redirect("home")

    booking = get_object_or_404(Booking, id=id)

    booking.status = "Approved"
    booking.save()

    messages.success(request, "Booking approved successfully.")

    return redirect("admin_bookings")


@login_required(login_url="login")
def reject_booking(request, id):

    if not request.user.is_staff:
        return redirect("home")

    booking = get_object_or_404(Booking, id=id)

    booking.status = "Rejected"
    booking.save()

    messages.success(request, "Booking rejected successfully.")

    return redirect("admin_bookings")
# =========================================================
# EDIT HOUSEBOAT
# =========================================================

@login_required(login_url="login")
def edit_houseboat(request, id):

    if not request.user.is_staff:
        messages.error(request, "You are not authorized.")
        return redirect("home")

    boat = get_object_or_404(
        ProfessionalHouseboatDataset500Rows,
        houseboatid=id
    )

    if request.method == "POST":

        form = HouseboatForm(
            request.POST,
            instance=boat
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Houseboat updated successfully."
            )

            return redirect("admin_houseboats")

    else:

        form = HouseboatForm(instance=boat)

    return render(
        request,
        "edit_houseboat.html",
        {
            "form": form,
            "boat": boat
        }
    )
# =========================================================
# DELETE HOUSEBOAT
# =========================================================

@login_required(login_url="login")
def delete_houseboat(request, id):

    if not request.user.is_staff:
        messages.error(request, "You are not authorized.")
        return redirect("home")

    boat = get_object_or_404(
        ProfessionalHouseboatDataset500Rows,
        houseboatid=id
    )

    boat.delete()

    messages.success(
        request,
        "Houseboat deleted successfully."
    )

    return redirect("admin_houseboats")
@login_required(login_url="login")
def edit_houseboat(request, id):

    if not request.user.is_staff:
        return redirect("home")

    boat = ProfessionalHouseboatDataset500Rows.objects.get(
        houseboatid=id
    )

    if request.method == "POST":

        form = HouseboatForm(
            request.POST,
            instance=boat
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Houseboat updated successfully."
            )

            return redirect("admin_houseboats")

    else:

        form = HouseboatForm(instance=boat)

    return render(
        request,
        "edit_houseboat.html",
        {
            "form": form,
            "boat": boat
        }
    )
def rag_chat(request):

    if request.method == "GET":
        return render(request, "rag.html")

    if request.method == "POST":

        try:

            data = json.loads(
                request.body
            )

            question = data.get(
                "question",
                ""
            ).strip()

            if not question:

                return JsonResponse({
                    "answer": "Please ask me something about the houseboats."
                })

            # Send question to RAG system
            answer = ask_rag(question)

            return JsonResponse({
                "answer": answer
            })

        except Exception as e:

            print("RAG ERROR:", e)

            return JsonResponse(
                {
                    "answer":
                    "Sorry, I couldn't process your question right now."
                },
                status=500
            )
from django.urls import path
from . import views


urlpatterns = [

    # =========================================================
    # HOME
    # =========================================================

    path(
        "",
        views.home,
        name="home"
    ),
path("rag/", views.rag_chat, name="rag_chat"),

    # =========================================================
    # ADMIN DASHBOARD
    # =========================================================

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    # =========================================================
    # ADMIN MANAGEMENT
    # =========================================================

    path(
        "admin-houseboats/",
        views.admin_houseboats,
        name="admin_houseboats"
    ),

    path(
        "admin-users/",
        views.admin_users,
        name="admin_users"
    ),

    path(
        "admin-bookings/",
        views.admin_bookings,
        name="admin_bookings"
    ),

    path(
        "admin-wishlist/",
        views.admin_wishlist,
        name="admin_wishlist"
    ),


    # =========================================================
  
path(
    "admin-contact-messages/",
    views.admin_contact_messages,
    name="admin_contact_messages"
),

path(
    "admin-contact-messages/read/<int:id>/",
    views.mark_contact_read,
    name="mark_contact_read"
),

path(
    "admin-contact-messages/delete/<int:id>/",
    views.delete_contact_message,
    name="delete_contact_message"
),

    # =========================================================
    # USER DASHBOARD
    # =========================================================

    path(
        "user-dashboard/",
        views.user_dashboard,
        name="user_dashboard"
    ),


    # =========================================================
    # HOUSEBOAT DETAILS
    # =========================================================

    path(
        "houseboat/<str:id>/",
        views.details,
        name="details"
    ),


    # =========================================================
    # AUTHENTICATION
    # =========================================================

    path(
        "login/",
        views.login_page,
        name="login"
    ),

    path(
        "register/",
        views.register_page,
        name="register"
    ),

    path(
        "logout/",
        views.logout_page,
        name="logout"
    ),


    # =========================================================
    # PAGES
    # =========================================================

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),


    # =========================================================
    # BOOKING
    # =========================================================

    path(
        "book/<str:id>/",
        views.book,
        name="book"
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),

    path(
        "booking/cancel/<int:id>/",
        views.cancel_booking,
        name="cancel_booking"
    ),


    # =========================================================
    # WISHLIST
    # =========================================================

    path(
        "wishlist/add/<str:id>/",
        views.add_wishlist,
        name="add_wishlist"
    ),

    path(
        "my-wishlist/",
        views.my_wishlist,
        name="my_wishlist"
    ),

    path(
        "wishlist/remove/<str:id>/",
        views.remove_wishlist,
        name="remove_wishlist"
    ),


    # =========================================================
    # AI PERSONALIZED RECOMMENDATION
    # =========================================================

    path(
        "ai-recommend/",
        views.recommend,
        name="recommend"
    ),
    path(
    "approve-booking/<int:id>/",
    views.approve_booking,
    name="approve_booking",
),

path(
    "reject-booking/<int:id>/",
    views.reject_booking,
    name="reject_booking",
),
path(
    "edit-houseboat/<str:id>/",
    views.edit_houseboat,
    name="edit_houseboat",
),

path(
    "delete-houseboat/<str:id>/",
    views.delete_houseboat,
    name="delete_houseboat",
),
path(
    "edit-houseboat/<str:boat_id>/",
    views.edit_houseboat,
    name="edit_houseboat"
),

]
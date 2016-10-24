from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from konfera.models.event import Event
from konfera.models.ticket import REQUESTED
from konfera.models.ticket_type import TicketType, ACTIVE, PRESS, AID, VOLUNTEER
from konfera.register.forms import RegistrationForm


def _register_ticket(request, event, ticket_type):
    context = dict()
    if ticket_type._get_current_status() != ACTIVE:
        messages.error(request, _('This ticket type is not available'))
        return redirect('event_details', event.slug)

    description_required = ticket_type in (VOLUNTEER, PRESS, AID)
    form = RegistrationForm(request.POST or None, description_required=description_required)

    if form.is_valid():
        new_ticket = form.save(commit=False)
        new_ticket.status = REQUESTED
        new_ticket.type = ticket_type
        new_ticket.save()

        messages.success(request, _('Thanks for registering...'))

        return redirect('event_details', event.slug)

    context['form'] = form
    context['type'] = ticket_type.attendee_type

    return render(request, 'konfera/registration_form.html', context=context)


def register_ticket(request, slug, ticket_uuid):
    event = get_object_or_404(Event, slug=slug)
    ticket_type = get_object_or_404(TicketType, event=event, uuid=ticket_uuid)

    return _register_ticket(request, event, ticket_type)

def _register_ticket_attendee(request, slug, attendee_type):
    event = get_object_or_404(Event, slug=slug)
    ticket_types = TicketType.objects.filter(event=event, attendee_type=attendee_type)

    if ticket_types and len(ticket_types) == 1 and ticket_types[0].status == ACTIVE:
        return _register_ticket(request, event, ticket_types[0])
    else:
        messages.warning(request, _('The ticket type is not available!'))
        return redirect('event_tickets', slug)


def register_ticket_volunteer(request, slug):
    return _register_ticket_attendee(request, slug, VOLUNTEER)


def register_ticket_press(request, slug):
    return _register_ticket_attendee(request, slug, PRESS)


def register_ticket_aid(request, slug):
    return _register_ticket_attendee(request, slug, AID)

"""Login stage logic"""
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext as _
from structlog import get_logger

from passbook.flows.planner import PLAN_CONTEXT_PENDING_USER
from passbook.flows.stage import StageView
from passbook.stages.password.stage import PLAN_CONTEXT_AUTHENTICATION_BACKEND

LOGGER = get_logger()


class UserLoginStageView(StageView):
    """Finalise Authentication flow by logging the user in"""

    def get(self, request: HttpRequest) -> HttpResponse:
        if PLAN_CONTEXT_PENDING_USER not in self.executor.plan.context:
            message = _("No Pending user to login.")
            messages.error(request, message)
            LOGGER.debug(message)
            return self.executor.stage_invalid()
        if PLAN_CONTEXT_AUTHENTICATION_BACKEND not in self.executor.plan.context:
            message = _("Pending user has no backend.")
            messages.error(request, message)
            LOGGER.debug(message)
            return self.executor.stage_invalid()
        backend = self.executor.plan.context[PLAN_CONTEXT_AUTHENTICATION_BACKEND]
        login(
            self.request,
            self.executor.plan.context[PLAN_CONTEXT_PENDING_USER],
            backend=backend,
        )
        self.request.session.set_expiry(self.executor.current_stage.session_duration)
        LOGGER.debug(
            "Logged in",
            user=self.executor.plan.context[PLAN_CONTEXT_PENDING_USER],
            flow_slug=self.executor.flow.slug,
            session_duration=self.executor.current_stage.session_duration,
        )
        return self.executor.stage_ok()

// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import ReactDOM from "react-dom";
import { InvenioRequestsApp } from "./InvenioRequestsApp";
import {
  TimelineAcceptEvent,
  TimelineCancelEvent,
  TimelineDeclineEvent,
  TimelineExpireEvent,
  TimelineUnknownEvent,
} from "./timelineEvents";
import {
  IconSubmitStatus,
  IconDeleteStatus,
  IconAcceptStatus,
  IconDeclineStatus,
  IconCancelStatus,
  IconExpireStatus,
} from "./request";
import { LabelTypeSubmission, LabelTypeInvitation } from "./request";
import {
  RequestAcceptButton,
  RequestCancelButton,
  RequestDeclineButton,
  RequestModalCancelButton,
} from "./components/Buttons";
import { i18next } from "@translations/invenio_requests/i18next";

const requestDetailsDiv = document.getElementById("request-detail");
const request = JSON.parse(requestDetailsDiv.dataset.record);
const defaultQueryParams = JSON.parse(
  requestDetailsDiv.dataset.defaultQueryConfig
);

const overriddenComponents = {
  "TimelineEvent.layout.unknown": TimelineUnknownEvent,
  "TimelineEvent.layout.declined": TimelineDeclineEvent,
  "TimelineEvent.layout.accepted": TimelineAcceptEvent,
  "TimelineEvent.layout.expired": TimelineExpireEvent,
  "TimelineEvent.layout.cancelled": TimelineCancelEvent,
  "RequestStatusIcon.layout.submitted": IconSubmitStatus,
  "RequestStatusIcon.layout.deleted": IconDeleteStatus,
  "RequestStatusIcon.layout.accepted": IconAcceptStatus,
  "RequestStatusIcon.layout.declined": IconDeclineStatus,
  "RequestStatusIcon.layout.cancelled": IconCancelStatus,
  "RequestStatusIcon.layout.expired": IconExpireStatus,
  "RequestTypeLabel.layout.community-submission": LabelTypeSubmission,
  "RequestTypeLabel.layout.community-invitation": LabelTypeInvitation,
  "RequestAction.button.cancel": RequestCancelButton,
  "RequestAction.button.accept": RequestAcceptButton,
  "RequestAction.button.decline": RequestDeclineButton,
  "RequestActionModal.button.cancel": RequestModalCancelButton,
  "RequestActionModal.button.accept": RequestAcceptButton,
  "RequestActionModal.button.decline": RequestDeclineButton,
  "RequestActionModal.title.cancel": () => i18next.t("Cancel request"),
  "RequestActionModal.title.accept": () => i18next.t("Accept request"),
  "RequestActionModal.title.decline": () => i18next.t("Decline request"),
  "RequestStatus.submitted": () => i18next.t("Submitted"),
  "RequestStatus.accepted": () => i18next.t("Accepted"),
  "RequestStatus.cancelled": () => i18next.t("Cancelled"),
  "RequestStatus.declined": () => i18next.t("Declined"),
  "RequestStatus.expired": () => i18next.t("Expired"),
};

ReactDOM.render(
  <InvenioRequestsApp
    request={request}
    defaultQueryParams={defaultQueryParams}
    overriddenCmps={overriddenComponents}
  />,
  requestDetailsDiv
);

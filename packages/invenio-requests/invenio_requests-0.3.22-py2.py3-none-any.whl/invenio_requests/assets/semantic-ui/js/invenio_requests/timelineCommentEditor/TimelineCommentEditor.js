// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import FormattedInputEditor from "../components/FormattedInputEditor";
import React from "react";
import { SaveButton } from "../components/Buttons";
import { Container, Message } from "semantic-ui-react";
import PropTypes from "prop-types";
import { i18next } from "@translations/invenio_requests/i18next";

const TimelineCommentEditor = ({
  isLoading,
  commentContent,
  setCommentContent,
  error,
  submitComment,
}) => {
  return (
    <div className="timeline-comment-editor-container">
      {error && <Message negative>{error}</Message>}
      <FormattedInputEditor
        data={commentContent}
        onChange={(event, editor) => setCommentContent(editor.getData())}
        minHeight="7rem"
      />
      <div className="text-align-right rel-mt-1">
        <SaveButton
          icon="send"
          size="medium"
          content={i18next.t("Comment")}
          loading={isLoading}
          onClick={() => submitComment(commentContent, "html")}
        />
      </div>
    </div>
  );
};

TimelineCommentEditor.propTypes = {
  commentContent: PropTypes.string,
  isLoading: PropTypes.bool,
  setCommentContent: PropTypes.func.isRequired,
  error: PropTypes.string,
  submitComment: PropTypes.func.isRequired,
};

TimelineCommentEditor.defaultProps = {
  commentContent: "",
  isLoading: false,
  error: "",
};

export default TimelineCommentEditor;

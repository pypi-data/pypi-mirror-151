/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import { i18next } from "@translations/invenio_communities/i18next";
import _isEmpty from "lodash/isEmpty";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { Image } from "react-invenio-forms";
import { Button, Header, Icon, Label, Segment } from "semantic-ui-react";

export class SelectedMembers extends Component {
  removeMember = (id) => {
    const { selectedMembers, updateSelectedMembers } = this.props;
    delete selectedMembers[id];
    updateSelectedMembers(selectedMembers);
  };

  render() {
    const { selectedMembers, displayingGroups } = this.props;

    return !_isEmpty(selectedMembers) ? (
      <>
        <Header as="h2" size="small">
          {i18next.t(displayingGroups ? "Selected groups" : "Selected members")}
        </Header>
        <Segment className="selected-members-header mb-20 mr-20">
          {Object.entries(selectedMembers).map(([memberId, member]) => (
            <Button
              key={memberId}
              className="p-0 mr-10"
              onClick={() => this.removeMember(memberId)}
              type="button"
              aria-label={i18next.t("remove {{name}}", {
                name: member.name,
              })}
            >
              <Label image>
                <Image src={member.avatar} alt="" aria-hidden={true} />
                {member.name}
                <Icon name="delete" />
              </Label>
            </Button>
          ))}
        </Segment>
      </>
    ) : (
      <div className="selected-members-header mb-20">
        <Segment placeholder>
          <Header icon>
            <Icon name="users" />

            {i18next.t(
              displayingGroups ? "No groups selected." : "No people selected."
            )}
          </Header>
        </Segment>
      </div>
    );
  }
}

SelectedMembers.propTypes = {
  selectedMembers: PropTypes.object.isRequired,
  updateSelectedMembers: PropTypes.func.isRequired,
  displayingGroups: PropTypes.bool,
};

SelectedMembers.defaultProps = {
  displayingGroups: false,
};

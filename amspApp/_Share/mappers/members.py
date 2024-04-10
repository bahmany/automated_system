class MembersMapper:
    def ProfileForGroups(self, PositionInstance, ProfileDocumentInstance):
        result = {}
        result["avatar"] = ProfileDocumentInstance.extra['profileAvatar']['url'] if "url" in \
                                                                                    ProfileDocumentInstance.extra[
                                                                                        'profileAvatar'] else None if "profileAvatar" in ProfileDocumentInstance.extra else None

        result["chartName"]= PositionInstance.chart.title
        result["positionID"]= PositionInstance.id
        result["profileID"]= str(ProfileDocumentInstance.id)
        result["userID"]= PositionInstance.user_id
        result["chartID"]= PositionInstance.chart.id
        result["profileName"]= ProfileDocumentInstance.extra['Name']

        return result

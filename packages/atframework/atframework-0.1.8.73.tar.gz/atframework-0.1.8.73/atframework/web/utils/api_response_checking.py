'''
Created on Mar 25, 2022

@author: Siro

'''

import json
from atframework.tools.log.config import logger


class ApiResponseChecking(object):

    """
    Check response for registration

    {
    "success": true,
    "t": "bb13cf8e15fd435a91e1b41562dfcb51"
    }

    """

    def check_response_registration(self, response_data):
        # json_data = json.dumps(response_data)
        families_dic = json.loads(response_data)

        logger.info(families_dic)

        registration_key_list = []
        registration_value_list = []
        for i, j in families_dic.items():
            registration_key_list.append(i)
            registration_value_list.append(j)
        # families key should be games
        for k in range(len(registration_key_list)):
            if registration_key_list[k] == "success":
                result = (registration_value_list[k])
                return result
        return False

    """
    Check response for games/family/favorites
    """

    def check_response_game_family_favorites(self, response_data):
        # json_data = json.dumps(response_data)
        families_dic = json.loads(response_data)

        families_key_list = []
        families_value_list = []
        for i, j in families_dic.items():
            families_key_list.append(i)
            families_value_list.append(j)
        # families key should be games
        assert families_key_list[0] == 'games'

        # print(key_list)
        family = families_value_list[0][0]

        family_key_list = []
        for k in family:
            family_key_list.append(k)
        logger.info(family_key_list)

        list_string = ['familyId', 'name', 'status', 'provider', 'translations']
        string_set = set(family_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    """
    Check response for /positioning
    """

    def check_response_positioning(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)

        positionings_key_list = []
        positionings_value_list = []
        for i, j in positioning_dic.items():
            positionings_key_list.append(i)
            positionings_value_list.append(j)
        # families key should be games
        assert positionings_key_list[0] == 'positioning'

        # print(key_list)
        positioning = positionings_value_list[0][0]

        positioning_key_list = []
        for k in positioning:
            positioning_key_list.append(k)
        logger.info(positioning_key_list)

        list_string = ['name', 'friendlyName', 'slug', 'tags', 'classifyName', 'classifyId', 'type', 'status', 'families',
                       'count', 'size', 'currentPage', 'pageCount']
        string_set = set(positioning_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

    """
    Check response for /positioning/{group}
    """

    def check_response_positioning_group(self, response_data):
        # json_data = json.dumps(response_data)
        positioning_dic = json.loads(response_data)

        positioning_key_list = []
        for k in positioning_dic.keys():
            positioning_key_list.append(k)
        logger.info(positioning_key_list)

        list_string = ['name', 'friendlyName', 'slug', 'tags', 'classifyName', 'classifyId', 'type', 'status',
                       'families', 'count', 'size', 'currentPage', 'pageCount']
        string_set = set(positioning_key_list)
        result = all([word in string_set for word in list_string])
        assert result
        return True

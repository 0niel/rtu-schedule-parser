from rtu_schedule_parser.constants import Campus


def test_schedule_data_0(excel_parser):
    schedule_data = excel_parser.parse()
    assert schedule_data.get_dataframe() is None
    assert len(schedule_data.get_groups()) > 0
    assert 'КРБО-01-19' in schedule_data.get_groups()
    assert 'ККСО-04-19' in schedule_data.get_groups()

    schedule_data.generate_dataframe()
    df = schedule_data.get_dataframe()
    assert schedule_data.get_dataframe() is not None
    assert len(df) > 0
    assert len(df.columns) > 0
    assert len(df[df['group'] == 'КРБО-01-19']) > 0
    assert len(df[df['group'] == 'ККСО-04-19']) > 0

    group_schedule = schedule_data.get_group_schedule('КРБО-01-19')
    assert group_schedule.lessons is not None
    assert len(group_schedule.lessons) > 0
    assert group_schedule.lessons[0].name is not None

    try:
        schedule = schedule_data.get_group_schedule('КРБО-01-22')
        assert False
    except ValueError:
        assert True

    # test get_rooms
    rooms = schedule_data.get_rooms()
    assert rooms is not None
    assert len(rooms) > 0
    first_room = rooms[0]
    assert first_room is not None
    assert first_room.name is not None
    assert first_room.campus == Campus.V_78

    campuses = [room.campus for room in rooms]
    campuses = set(campuses)
    assert len(campuses) > 2
    assert Campus.V_78 in campuses
    assert Campus.SG_22 in campuses

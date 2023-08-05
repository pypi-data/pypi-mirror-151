from levatas_alira_cli.alr import CLI


def test_version_check():
    cli = CLI(
        {
            "metadata": {
                "GITHUB_REPOSITORY_ACCESS_USER": "user",
                "GITHUB_REPOSITORY_ACCESS_TOKEN": "token",
            },
            "not_valid_after": "2020-01-01",
        },
        None,
        None,
        None,
        None,
    )

    assert not cli._is_upgrade_warning_necessary(
        {"license_version": "v1.0.0", "version": "1.0.0"}
    )
    assert cli._is_upgrade_warning_necessary(
        {"license_version": "v1.0.0", "version": "1.0.2"}
    )

    assert not cli._is_upgrade_warning_necessary(
        {"license_version": "1.0", "version": "1.0.2"}
    )

# CloudWatch Logs Retention Setter

This Python script allows you to set the retention period for all your CloudWatch log groups in an automated manner.

## Requirements

- Python 3.x installed on your system.
- AWS CLI configured with valid credentials in your local environment.


## Usage

1. Run the `SetRetentionDays.py` script with the following command:

    ```
    python SetRetentionDays.py [RETENTION]
    ```

    Where `[RETENTION]` is the retention period in days you wish to set for your CloudWatch logs. It must be an integer value from the following:

    - 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653.

    For example, to set a retention period of 30 days, run:

    ```
    python SetRetentionDays.py 30
    ```

2. The script will display the progress and result of the retention configuration for each CloudWatch log group.

## Contributions

If you encounter any issues or have any improvements, feel free to open an issue or send a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

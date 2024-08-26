import PropTypes from 'prop-types';

const ErrorInput = ({message}) => {
    return (
        <div className="text-xs text-red-500 pt-1">{message}</div>
    )
}

ErrorInput.propTypes = {
    message: PropTypes.string.isRequired,
};

export default ErrorInput;
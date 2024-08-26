import PropTypes from 'prop-types';

const Button = (props) => {
    return (
        <div
            className={`p-3 text-primary rounded cursor-pointer text-center hover:text-white hover:bg-primary hover:opacity-80 ${props?.styles}`}
            style={{
                border: props.border && '1px solid #00aad3',
                backgroundColor: props.backgroundColor && '#00aad3',
                color: props.backgroundColor && '#fff',
            }}
            onClick={props.onClick}
        >
            {props.text}
        </div>
    );
};

Button.propTypes = {
    styles: PropTypes.string,
    border: PropTypes.bool,
    backgroundColor: PropTypes.bool,
    text: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
};

export default Button;

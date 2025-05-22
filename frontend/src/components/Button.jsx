function Button({ children, onClick, disabled, variant = "primary" }) {
  const baseStyles =
    "px-4 py-2 rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors";
  const variantStyles = {
    primary: "bg-secondary text-white hover:bg-blue-700 focus:ring-secondary",
    success: "bg-accent text-white hover:bg-green-700 focus:ring-accent",
    danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-600",
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

export default Button;

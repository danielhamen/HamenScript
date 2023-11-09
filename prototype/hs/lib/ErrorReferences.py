ErrorReferences = {
    "x0001": ["OperatorError", lambda : "Invalid operation employed for defining/modifying a variable; consider utilizing an assignment operator instead"],
    "x0002": ["DeclarationError", lambda : "Attempting to redefine an existing variable is not permissible; the `let` and `const` keywords are intended for defining variables that do not already exist."],
    "x0003": ["ReservedKeywordError", lambda kwd : f"Invalid variable definition using a reserved keyword, `{kwd}`; consider using an alternative identifier"],
    "x0004": ["IOStreamWritingError", lambda : "Inappropriate utilization of the stdout keyword; this keyword should precede exactly one value"],
    "x0005": ["VariableNotDefinedError", lambda variable_name : f"Unauthorized assignment to a non-existent variable, {variable_name}"],
    "x0006": ["ConstantAssignmentError", lambda variable_name : f"Unauthorized assignment of a constant variable, {variable_name}; constants are immutable and cannot be reassigned"],
    "x0007": ["StrictTypeViolationError", lambda variable_name,variable_type,target_type : f"Unauthorized attempt to reassign a variable with strict typing; variable {variable_name} cannot be reassigned from type {variable_type} to {target_type}; it must adhere to the type {target_type}"],
    "x0008": ["VariableNameDeclarationError", lambda variable_name : f"Unauthorized attempt to declare a variable, {variable_name}; the provided name or type is invalid"],
    "x0009": ["ReferenceError", lambda variable_name : f"Attempted resolution of a non-existent token or symbol; the variable named {variable_name} has not been declared within the local or global scope"],
    "x0010": ["MisplacedCatchError", lambda : f"The usage of the `try`/`catch` statement is invalid; it is impermissible to employ a `catch` clause without an antecedent `try` block defined for error handling"],
}
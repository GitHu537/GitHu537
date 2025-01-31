export default function FileUpload({ onUpload }) {
    const handleUpload = async (event) => {
        event.preventDefault();
        // File upload logic here...
        onUpload();
    };

    return (
        <form onSubmit={handleUpload}>
            {/* Form fields for username, file category, etc. */}
        </form>
    );
}
export default function FileQuery({ onQuery }) {
    const handleQuery = async (event) => {
        event.preventDefault();
        // Query logic here...
        onQuery();
    };

    return (
        <form onSubmit={handleQuery}>
            {/* Form fields for username query */}
        </form>
    );
}
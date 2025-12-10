
exports.handler = async (event) => {
  console.log("Space Canvas event:", JSON.stringify(event));
  return {
    statusCode: 200,
    body: JSON.stringify({
      message: "Hello from Space Canvas Lambda (dummy)!"
    })
  };
};

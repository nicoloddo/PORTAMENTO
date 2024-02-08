# Build and Deploy.
# Remember that the samconfig must have resolve_image_repos = true or it won't find the images repos: not even if you specify them with image_repositories = []

& cd ..
& sam build
& sam deploy

pause
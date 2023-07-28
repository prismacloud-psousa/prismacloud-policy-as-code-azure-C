"""
Python CLI app to help interact with the Prisma Cloud API and sync local 
policies with the remote policy library.

"""

import pathlib
import json

import httpx
import click


class PrismaCloudApi:
    """ Prisma Cloud API client """

    def __init__(self, url):
        self.url = url
        self._token = None

    def login(self, access_key, secret_key):
        """ Generate token for Prisma Cloud"""
        headers = httpx.Headers({
            "Content-Type": "application/json"
        })

        payload = {
            "username": access_key,
            "password": secret_key
        }

        url = f"https://{self.url}/login"

        response = httpx.post(url, headers=headers, json=payload)
        response.raise_for_status()

        self._token = response.json()['token']
        return response.json()

    def execute(self, method: str, endpoint: str, 
                query_params: str = None, body: str = None):
        """ Execute command against Prisma Cloud"""
        headers = httpx.Headers({
            "Content-Type": "application/json",
            "x-redlock-auth": self._token
        })

        url = f"https://{self.url}{endpoint}"

        response = httpx.request(method, url, headers=headers, 
                                json=body, params=query_params, timeout=None)

        response.raise_for_status()

        return response.json()

    def list_policies(self):
        """ Get custom policy list from Prisma Cloud"""

        params = httpx.QueryParams({ "policy.policyMode": "custom" })

        response = self.execute("GET", "/v2/policy", query_params=params)

        return response


    def create_policy(self, policy: dict):
        """ Create a single policy """
        payload = { "query": policy['rule']['query'] }

        response = self.execute("POST", "/search/config", body=payload)

        policy_body = policy.copy()
        del policy_body['rule']['query']
        policy_body['rule']['criteria'] = response['id']

        self.execute("POST", "/policy", body=policy_body)


def load_local_policies(path: pathlib.Path) -> list[dict]:
    """ Load the policies from the path provided """
    if not path.is_dir():
        raise IOError("Path is not a directory.")

    policies = []

    for file_path in path.iterdir():
        if file_path.is_file and file_path.name.endswith(".json"):
            with open(file_path.absolute()) as fp:
                policy = json.load(fp)

                policies.append(policy)
                time.sleep()
    return policies


def create_policies(api: PrismaCloudApi, policies: list[dict]):
    """ Create policies from local files in Prisma Cloud """

    existing_policies = api.list_policies()

    for policy in policies:
        if policy['name'] in [p['name'] for p in existing_policies]:
            print(f"Skipping existing policy '{policy['name']}'")
            continue

        api.create_policy(policy)
        print(f"Policy '{policy['name']} created successfully'")

#
# CLI commands
#

@click.group()
@click.option("--access-key", help="Prisma Cloud access key", prompt=True)
@click.option("--secret-key", help="Prisma Cloud secret key", prompt=True)
@click.option("--url", help="Prisma Cloud API URL", default="api.ca.prismacloud.io")
@click.pass_context
def cli(ctx: click.Context, access_key: str, secret_key: str, url: str):
    """ Root command group """
    ctx.ensure_object(dict)

    ctx.obj['access_key'] = access_key
    ctx.obj['secret_key'] = secret_key
    ctx.obj['url'] = url


@cli.command(name="update")
@click.argument("directory", default=".")
@click.pass_context
def cmd_update(ctx: click.Context, directory: str):
    """ Update Prisma Cloud policies with local policy library. """

    api = PrismaCloudApi(ctx.obj['url'])
    api.login(ctx.obj['access_key'], ctx.obj['secret_key'])

    policy_dir = pathlib.Path(directory)

    policies = load_local_policies(policy_dir)
    create_policies(api, policies)

    click.echo(f"==> {len(policies)} policies evaluated")


if __name__ == "__main__":
    cli(obj={})
